from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.order.enums import OrderStatusEnum, OrderTypeEnum, PaymentMethodEnum


class OrderModel(BaseModel):
    Status = OrderStatusEnum
    PaymentMethod = PaymentMethodEnum
    Type = OrderTypeEnum

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("User"),
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    payment_method = models.CharField(
        _("Payment Method"),
        max_length=20,
        choices=PaymentMethod.choices,
        null=True,
        blank=True,
    )

    order_type = models.CharField(
        max_length=20,
        choices=Type.choices,
    )

    total_amount = models.DecimalField(
        _("Total Amount"),
        max_digits=18,
        decimal_places=0,
        default=0,
    )

    locked_price_at = models.DateTimeField(
        _("Locked Price At"),
        null=True,
        blank=True,
    )

    expire_at = models.DateTimeField(
        _("Expire At"),
        null=True,
        blank=True,
    )

    invoice_generated = models.BooleanField(
        _("Invoice Generated"),
        default=False,
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def str(self):
        return f"Order - {self.user.phone_number} - {self.status}"


class OrderItemModel(BaseModel):
    order = models.ForeignKey(
        "order.OrderModel",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Order"),
    )

    product = models.ForeignKey(
        "product.ProductModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
        verbose_name=_("Product"),
    )

    coin = models.ForeignKey(
        "product.CoinModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
        verbose_name=_("Coin"),
    )

    gold_amount = models.DecimalField(max_digits=18, decimal_places=3, default=0)

    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    unit_price = models.DecimalField(_("Unit Price"), max_digits=18, decimal_places=0)
    total_price = models.DecimalField(_("Total Price"), max_digits=18, decimal_places=0)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def clean(self):
        super().clean()

        if self.gold_amount > 0:
            if self.product or self.coin:
                raise ValidationError(
                    _("Weight-based items cannot have product or coin.")
                )
            return

        if not self.product and not self.coin:
            raise ValidationError(_("You must select either a product or a coin."))

        selected = [self.product, self.coin]

        if sum(1 for x in selected if x) > 1:
            raise ValidationError(_("You cannot select more than one item type."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Item {self.id} - Order {self.order.id}"


class InvoiceModel(BaseModel):
    order = models.OneToOneField(
        "order.OrderModel",
        on_delete=models.CASCADE,
        related_name="invoice",
        verbose_name=_("Order"),
    )

    invoice_number = models.CharField(_("Invoice Number"), max_length=50, unique=True)
    title = models.CharField(_("Title"), max_length=100, blank=True, null=True)
    amount = models.DecimalField(_("Amount"), max_digits=18, decimal_places=0)
    tax_amount = models.DecimalField(
        _("Tax Amount"), max_digits=18, decimal_places=0, default=0
    )
    wage_amount = models.DecimalField(
        _("Wage Amount"), max_digits=18, decimal_places=0, default=0
    )

    is_paid = models.BooleanField(_("Paid"), default=False)
    paid_at = models.DateTimeField(_("Paid At"), blank=True, null=True)

    weight = models.DecimalField(max_digits=18, decimal_places=3, default=0)

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.amount}"
