from apps.core.models import BaseModel
from apps.wallet.enums import (
    CoinTypeEnum,
    WalletTransactionTypeEnum,
    WithdrawStatusEnum,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class WalletModel(BaseModel):
    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="wallet",
        verbose_name=_("User"),
    )
    balance = models.DecimalField(
        _("Balance"), max_digits=18, decimal_places=0, default=0
    )

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

    def __str__(self):
        return f"{self.user.phone_number} - {self.balance}"


class WalletTransactionModel(BaseModel):
    Type = WalletTransactionTypeEnum

    wallet = models.ForeignKey(
        "wallet.WalletModel",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name=_("Wallet"),
    )
    amount = models.DecimalField(_("Amount"), max_digits=18, decimal_places=0)
    transaction_type = models.CharField(
        _("Transaction Type"),
        max_length=20,
        choices=Type.choices,
    )
    description = models.CharField(
        _("Description"), max_length=200, blank=True, null=True
    )
    is_success = models.BooleanField(_("Success"), default=True)

    class Meta:
        verbose_name = _("Wallet Transaction")
        verbose_name_plural = _("Wallet Transactions")

    def __str__(self):
        return (
            f"{self.wallet.user.phone_number} - {self.amount} - {self.transaction_type}"
        )


class WithdrawRequestModel(BaseModel):
    Status = WithdrawStatusEnum

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="withdraw_requests",
        verbose_name=_("User"),
    )
    amount = models.DecimalField(_("Amount"), max_digits=18, decimal_places=0)
    status = models.CharField(
        _("Status"), max_length=20, choices=Status.choices, default=Status.PENDING
    )
    admin_note = models.CharField(
        _("Admin Note"), max_length=200, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Withdraw Request")
        verbose_name_plural = _("Withdraw Requests")

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount} - {self.status}"


class GoldInventoryModel(BaseModel):
    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="gold_inventories",
        verbose_name=_("User"),
    )
    amount = models.DecimalField(
        _("Amount (germs or units)"), max_digits=18, decimal_places=3, default=0
    )

    class Meta:
        verbose_name = _("Gold Inventory")
        verbose_name_plural = _("Gold Inventories")

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount}"


class CoinInventoryModel(BaseModel):
    Type = CoinTypeEnum

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="coin_inventories",
        verbose_name=_("User"),
    )
    coin_type = models.CharField(
        _("Coin Type"),
        max_length=20,
        choices=Type.choices,
    )
    amount = models.PositiveIntegerField(_("Amount"), default=0)

    class Meta:
        verbose_name = _("Coin Inventory")
        verbose_name_plural = _("Coin Inventories")

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount}"
