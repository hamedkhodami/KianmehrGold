from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.order.enums import OrderStatusEnum
from apps.order.models import InvoiceModel
from apps.payment.enums import PaymentStatusEnum
from apps.payment.models import PaymentModel
from apps.wallet.enums import WalletTransactionTypeEnum
from apps.wallet.models import WalletTransactionModel


@transaction.atomic
def gateway_callback(request):

    authority = request.GET.get("authority")

    status = request.GET.get("status")

    payment = (
        PaymentModel.objects.select_for_update()
        .select_related("order", "wallet_charge", "user")
        .get(authority=authority)
    )

    # قبلا پرداخت شده
    if payment.status == PaymentStatusEnum.SUCCESS:

        messages.warning(request, _("Payment already processed."))

        return redirect("/")

    # منقضی شده
    if payment.expire_at:

        if timezone.now() > payment.expire_at:

            payment.status = PaymentStatusEnum.FAILED

            payment.save()

            if payment.order:

                payment.order.status = OrderStatusEnum.CANCELED

                payment.order.save()

            if hasattr(payment, "wallet_charge"):

                payment.wallet_charge.status = PaymentStatusEnum.FAILED

                payment.wallet_charge.save()

            messages.error(request, _("Payment expired."))

            return redirect("/")

    # برگشت ناموفق از درگاه

    if status != "success":

        payment.status = PaymentStatusEnum.FAILED

        payment.save()

        if payment.order:

            payment.order.status = OrderStatusEnum.CANCELED

            payment.order.save()

        if hasattr(payment, "wallet_charge"):

            payment.wallet_charge.status = PaymentStatusEnum.FAILED

            payment.wallet_charge.save()

        messages.error(request, _("Payment failed."))

        return redirect("/")

    #################################################
    # پرداخت موفق
    #################################################

    payment.status = PaymentStatusEnum.SUCCESS

    payment.ref_id = "TEST_REF_ID"

    payment.save()

    #################################################
    # خرید محصول یا سکه
    #################################################

    if payment.order:

        order = payment.order

        item = order.items.select_for_update().select_related("product", "coin").first()

        if not item:

            messages.error(request, _("Order item not found."))

            return redirect("/")

        # محصول

        if item.product:

            product = item.product

            if product.stock < item.quantity:

                messages.error(request, _("Product stock is not enough."))

                return redirect("/")

            product.stock -= item.quantity

            product.save()

        # سکه

        elif item.coin:

            coin = item.coin

            if coin.stock < item.quantity:

                messages.error(request, _("Coin stock is not enough."))

                return redirect("/")

            coin.stock -= item.quantity

            coin.save()

        order.status = OrderStatusEnum.PAID

        order.save()

        InvoiceModel.objects.get_or_create(
            order=order,
            defaults={
                "invoice_number": f"INV-{order.id}",
                "amount": order.total_amount,
                "is_paid": True,
                "paid_at": timezone.now(),
            },
        )

        messages.success(request, _("Payment successful."))

        return redirect("/")

    #################################################
    # شارژ کیف پول
    #################################################

    if hasattr(payment, "wallet_charge"):

        wallet_charge = payment.wallet_charge

        wallet = payment.user.wallet

        wallet.balance += wallet_charge.amount

        wallet.save()

        WalletTransactionModel.objects.create(
            wallet=wallet,
            amount=wallet_charge.amount,
            transaction_type=WalletTransactionTypeEnum.DEPOSIT,
            description=_("Wallet charged from gateway"),
            is_success=True,
        )

        wallet_charge.status = PaymentStatusEnum.SUCCESS

        wallet_charge.save()

        messages.success(request, _("Wallet charged successfully."))

        return redirect("wallet:wallet_dashboard")

    return redirect("/")
