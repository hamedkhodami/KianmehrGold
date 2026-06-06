from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class OrderStatusEnum(TextChoices):
    PENDING = "pending", _("Pending")
    PAID = "paid", _("Paid")
    CANCELED = "canceled", _("Canceled")
    COMPLETED = "completed", _("Completed")


class PaymentMethodEnum(TextChoices):
    WALLET = "wallet", _("Wallet")
    GATEWAY = "gateway", _("Gateway")
    CASH = "cash", _("Cash Payment")


class OrderTypeEnum(TextChoices):
    BUY = "buy", _("Buy")
    SELL = "sell", _("Sell")
