from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class WalletTransactionTypeEnum(TextChoices):
    DEPOSIT = "deposit", _("Deposit")
    WITHDRAW = "withdraw", _("Withdraw")
    BUY = "buy", _("Buy")
    SELL = "sell", _("Sell")


class WithdrawStatusEnum(TextChoices):
    PENDING = "pending", _("Pending")
    PAID = "paid", _("Paid")
    REJECTED = "rejected", _("Rejected")
