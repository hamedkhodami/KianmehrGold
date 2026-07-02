from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify

from apps.core.models import BaseModel
from apps.product.enums import CoinTypeEnum, ProductStatusEnum
from apps.product.service.pricing_service import PriceService


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

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, separator="-", allow_unicode=True)
            slug = base_slug
            counter = 1

            while CategoryModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


# TODO : complete final price in next phase
class ProductModel(BaseModel):
    Status = ProductStatusEnum

    category = models.ForeignKey(
        "product.CategoryModel",
        on_delete=models.CASCADE,
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
    wage_percent = models.DecimalField(_("Wage (%)"), max_digits=5, decimal_places=2)
    tax_percent = models.DecimalField(_("Tax (%)"), max_digits=5, decimal_places=2)

    stock = models.PositiveIntegerField(default=0, verbose_name=_("Stock"))

    status = models.CharField(
        _("Status"), max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )

    description = models.TextField(_("Description"), blank=True, null=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        latest_price = GoldPriceModel.objects.filter(is_active=True).last()
        if not latest_price:
            return None

        return PriceService.calculate_final_price(
            self.weight, self.wage_percent, self.tax_percent, latest_price.gold_melted
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, separator="-", allow_unicode=True)
            slug = base_slug
            counter = 1

            while ProductModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        if self.stock <= 0:
            self.status = ProductStatusEnum.OUT_OF_STOCK
        else:
            self.status = ProductStatusEnum.AVAILABLE

        super().save(*args, **kwargs)


class CoinModel(BaseModel):
    Type = CoinTypeEnum
    Status = ProductStatusEnum

    coin_type = models.CharField(_("Coin Type"), max_length=20, choices=Type.choices)
    image = models.ImageField(
        _("Image"), upload_to="product/images", blank=True, null=True
    )
    weight = models.DecimalField(
        _("Weight (grams)"), max_digits=10, decimal_places=3, default=0
    )

    stock = models.PositiveIntegerField(_("Stock"), default=0)

    status = models.CharField(
        _("Status"), max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )

    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Coin")
        verbose_name_plural = _("Coins")
        unique_together = ("coin_type",)

    def __str__(self):
        return f"{self.coin_type}"

    @property
    def final_price(self):
        latest = GoldPriceModel.objects.filter(is_active=True).last()
        if not latest:
            return None

        mapping = {
            CoinTypeEnum.EMAMI: latest.emami_coin,
            CoinTypeEnum.FULL: latest.full_coin,
            CoinTypeEnum.HALF: latest.half_coin,
            CoinTypeEnum.QUARTER: latest.quarter_coin,
        }

        return mapping.get(self.coin_type)

    def save(self, *args, **kwargs):
        if self.stock <= 0:
            self.status = ProductStatusEnum.OUT_OF_STOCK
        else:
            self.status = ProductStatusEnum.AVAILABLE

        super().save(*args, **kwargs)


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

    is_active = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = _("Gold Price")
        verbose_name_plural = _("Gold Prices")

    def str(self):
        return f"Gold Price - {self.created_at}"
