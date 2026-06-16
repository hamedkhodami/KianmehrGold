from apps.order.models import InvoiceModel
from apps.payment.enums import PaymentStatusEnum
from apps.payment.models import PaymentModel
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def gateway_start(request, payment_id):
    payment = get_object_or_404(PaymentModel, id=payment_id)

    if payment.expire_at and timezone.now() > payment.expire_at:
        payment.status = PaymentStatusEnum.FAILED
        payment.save()
        return redirect("payment:expired")

    authority = "TEST_AUTH_CODE"

    payment.authority = authority
    payment.save()

    return redirect(f"/payment/fake-gateway/?authority={authority}")


@transaction.atomic
def gateway_callback(request):
    authority = request.GET.get("authority")
    status = request.GET.get("status")  # فرضاً success / failed

    payment = PaymentModel.objects.select_for_update().get(authority=authority)

    # اگر منقضی شده باشد
    if payment.expire_at and timezone.now() > payment.expire_at:
        payment.status = PaymentStatusEnum.FAILED
        payment.save()
        messages.error(request, _("Payment expired. Please try again."))
        return redirect("product:product_detail", slug=payment.product.slug)

    if status != "success":
        payment.status = PaymentStatusEnum.FAILED
        payment.save()
        messages.error(request, _("Payment failed."))
        return redirect("product:product_detail", slug=payment.product.slug)

    # 🔹 پرداخت موفق
    payment.status = PaymentStatusEnum.SUCCESS
    payment.ref_id = "TEST_REF_ID"
    payment.save()

    # 🔹 کم کردن موجودی محصول
    product = payment.product
    if product.stock <= 0:
        messages.error(request, _("Product is out of stock."))
        return redirect("product:product_detail", slug=product.slug)

    product.stock -= 1
    product.save()

    # 🔹 ساخت فاکتور با داده‌های قفل‌شده
    InvoiceModel.objects.create(
        order=None,  # چون این سناریو مستقل از Order است
        invoice_number=f"INV-P-{payment.id}",
        amount=payment.amount,
        tax_amount=payment.tax_amount,
        wage_amount=payment.wage_amount,
        locked_gold_price=payment.locked_gold_price,
        weight=payment.weight,
        is_paid=True,
        paid_at=timezone.now(),
    )

    messages.success(request, _("Payment successful. Your purchase is completed."))
    return redirect("product:product_detail", slug=product.slug)


# TODO: delete this after get real gateway
def fake_gateway(request):
    authority = request.GET.get("authority")

    # این صفحه فقط یک دکمه دارد که پرداخت موفق را شبیه‌سازی می‌کند
    return render(request, "payment/fake_gateway.html", {"authority": authority})
