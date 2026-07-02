from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.payment.enums import PaymentStatusEnum
from apps.payment.models import PaymentModel
from apps.payment.services.behpardakht_service import BehpardakhtService


def gateway_start(request, payment_id):

    payment = get_object_or_404(PaymentModel, id=payment_id)

    if payment.status != PaymentStatusEnum.PENDING:

        messages.error(request, _("This payment is already processed."))

        return redirect("/")

    if payment.expire_at:

        if timezone.now() > payment.expire_at:

            payment.status = PaymentStatusEnum.FAILED

            payment.save()

            messages.error(request, _("Payment expired."))

            return redirect("/")

    result = BehpardakhtService.request_payment(payment)

    if not result["success"]:

        messages.error(request, _("Could not connect to payment gateway."))

        return redirect("/")

    payment.authority = result["authority"]

    payment.save(update_fields=["authority"])

    return redirect(result["gateway_url"])
