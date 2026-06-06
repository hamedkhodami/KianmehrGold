from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class PaymentStatusEnum(TextChoices):
    PENDING = "pending", _("Pending")
    SUCCESS = "success", _("Success")
    FAILED = "failed", _("Failed")
    CANCELED = "canceled", _("Canceled")


class PaymentTypeEnum(TextChoices):
    ORDER = "order", _("Order Payment")
    WALLET_CHARGE = "wallet_charge", _("Wallet Charge")
