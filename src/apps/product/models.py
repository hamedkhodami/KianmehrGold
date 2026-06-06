from apps.core.models import BaseModel
from apps.product.enums import ProductStatusEnum
from apps.wallet.enums import CoinTypeEnum
from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoryModel(BaseModel):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    icon = models.ImageField(
        _("Icon"), upload_to="product/icons", blank=True, null=True
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title


# TODO : complete final price in next phase
# TODO : meta_title meta_description in phase4
class ProductModel(BaseModel):
    Status = ProductStatusEnum

    category = models.ForeignKey(
        "product.CategoryModel",
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
        verbose_name=_("Category"),
    )

    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)

    image = models.ImageField(
        _("Image"), upload_to="product/images", blank=True, null=True
    )

    weight = models.DecimalField(_("Weight (grams)"), max_digits=10, decimal_places=3)
    wage_percent = models.DecimalField(_("Wage (%)"), max_digits=5, decimal_places=4)
    tax_percent = models.DecimalField(_("Tax (%)"), max_digits=5, decimal_places=4)

    status = models.CharField(
        _("Status"), max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )

    description = models.TextField(_("Description"), blank=True, null=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title


class CoinModel(BaseModel):
    Type = CoinTypeEnum

    coin_type = models.CharField(_("Coin Type"), max_length=20, choices=Type.choices)
    image = models.ImageField(
        _("Image"), upload_to="product/images", blank=True, null=True
    )

    buy_price = models.DecimalField(_("Buy Price"), max_digits=18, decimal_places=0)
    sell_price = models.DecimalField(_("Sell Price"), max_digits=18, decimal_places=0)

    weight = models.DecimalField(
        _("Weight (grams)"), max_digits=10, decimal_places=3, default=0
    )

    stock = models.PositiveIntegerField(_("Stock"), default=0)

    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Coin")
        verbose_name_plural = _("Coins")
        unique_together = ("coin_type",)

    def str(self):
        return f"{self.coin_type} - {self.sell_price}"


class GoldPriceModel(BaseModel):
    gold_melted = models.DecimalField(
        _("Melted Gold Price"), max_digits=18, decimal_places=0
    )
    gold_ounce = models.DecimalField(
        _("Gold Ounce Price"), max_digits=18, decimal_places=0
    )
    gold_mozanneh = models.DecimalField(
        _("Muzanneh Price"), max_digits=18, decimal_places=0
    )

    quarter_coin = models.DecimalField(
        _("Quarter Coin Price"), max_digits=18, decimal_places=0
    )
    half_coin = models.DecimalField(
        _("Half Coin Price"), max_digits=18, decimal_places=0
    )
    full_coin = models.DecimalField(
        _("Full Coin Price"), max_digits=18, decimal_places=0
    )
    emami_coin = models.DecimalField(
        _("Emami Coin Price"), max_digits=18, decimal_places=0
    )

    class Meta:
        verbose_name = _("Gold Price")
        verbose_name_plural = _("Gold Prices")

    def str(self):
        return f"Gold Price - {self.created_at}"
