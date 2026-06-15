from apps.core.models import BaseModel
from apps.payment.enums import PaymentStatusEnum, PaymentTypeEnum
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentModel(BaseModel):
    Status = PaymentStatusEnum
    Type = PaymentTypeEnum

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("User"),
    )

    payment_type = models.CharField(
        _("Payment Type"), max_length=20, choices=Type.choices
    )

    order = models.ForeignKey(
        "order.OrderModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name=_("Order"),
    )

    product = models.ForeignKey(
        "product.ProductModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name=_("Product"),
    )

    amount = models.DecimalField(_("Amount"), max_digits=18, decimal_places=0)

    status = models.CharField(
        _("Status"), max_length=20, choices=Status.choices, default=Status.PENDING
    )

    authority = models.CharField(
        _("Authority Code"), max_length=255, blank=True, null=True
    )

    ref_id = models.CharField(_("Reference ID"), max_length=255, blank=True, null=True)

    expire_at = models.DateTimeField(_("Expire At"), null=True, blank=True)

    locked_gold_price = models.DecimalField(
        _("Locked Gold Price"),
        max_digits=18,
        decimal_places=0,
        default=0,
        null=True,
        blank=True,
    )
    wage_amount = models.DecimalField(
        _("Wage Amount"), max_digits=18, decimal_places=0, default=0
    )
    tax_amount = models.DecimalField(
        _("Tax Amount"), max_digits=18, decimal_places=0, default=0
    )
    weight = models.DecimalField(
        _("Weight"), max_digits=18, decimal_places=3, default=0
    )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def clean(self):

        if self.payment_type == self.Type.ORDER and not self.order:
            raise ValidationError(_("Order payment must have an order."))

        if self.payment_type == self.Type.WALLET_CHARGE and self.order:
            raise ValidationError(_("Wallet charge cannot have an order."))

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount} - {self.status}"


class WalletChargeModel(BaseModel):
    Status = PaymentStatusEnum

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="wallet_charges",
        verbose_name=_("User"),
    )

    amount = models.DecimalField(_("Amount"), max_digits=18, decimal_places=0)

    status = models.CharField(
        _("Status"), max_length=20, choices=Status.choices, default=Status.PENDING
    )

    payment = models.OneToOneField(
        "payment.PaymentModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wallet_charge",
        verbose_name=_("Payment"),
    )

    class Meta:
        verbose_name = _("Wallet Charge")
        verbose_name_plural = _("Wallet Charges")

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount} - {self.status}"
