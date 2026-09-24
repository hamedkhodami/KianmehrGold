from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from slugify import slugify

from apps.core.models import BaseModel
from apps.product.enums import (
    CoinCategoryEnum,
    CoinTypeEnum,
    ProductStatusEnum,
)
from apps.product.service.normal_coin_pricing import NormalCoinPricingService
from apps.product.service.parsian_pricing_service import ParsianPricingService
from apps.product.service.pricing_service import PriceService


class CategoryModel(BaseModel):
    title = models.CharField(_("Title"), max_length=255, unique=True)
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
        _("Image"), upload_to="product/product/images", blank=True, null=True
    )

    weight = models.DecimalField(_("Weight (grams)"), max_digits=10, decimal_places=3)
    wage_percent = models.DecimalField(_("Wage (%)"), max_digits=5, decimal_places=2)
    tax_percent = models.DecimalField(_("Tax (%)"), max_digits=5, decimal_places=2)

    profit_percent = models.DecimalField(
        _("Profit (%)"),
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text=_("Seller profit percentage on base + wage"),
    )

    status = models.CharField(
        _("Status"), max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )

    description = models.TextField(_("Description"), blank=True, null=True)
    stock = models.PositiveIntegerField(_("Stock"), default=0)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        from apps.product.service.price_cache_service import PriceCacheService

        latest_price = PriceCacheService.get_latest_price()
        if not latest_price:
            return None

        return PriceService.calculate_final_price(
            weight=self.weight,
            wage_percent=self.wage_percent,
            tax_percent=self.tax_percent,
            gold_price=latest_price.gold_melted,
            profit_percent=self.profit_percent,
        )

    @classmethod
    def aggregate_total_stock(cls):
        result = cls.objects.aggregate(total=Sum("stock"))
        return result["total"] or 0

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
    Status = ProductStatusEnum
    Type = CoinTypeEnum
    Category = CoinCategoryEnum

    category = models.CharField(_("Category"), max_length=20, choices=Category.choices)

    coin_type = models.CharField(
        _("Coin Type"), max_length=20, choices=Type.choices, null=True, blank=True
    )

    image = models.ImageField(
        _("Image"), upload_to="product/coin/images", blank=True, null=True
    )

    # فقط برای پارسیان
    weight = models.DecimalField(
        _("Weight (grams)"), max_digits=10, decimal_places=3, null=True, blank=True
    )

    # فقط برای سکه‌های عادی (MARKET)
    market_extra_fee = models.DecimalField(
        _("Extra Fee (Toman)"),
        max_digits=18,
        decimal_places=0,
        null=True,
        blank=True,
        help_text=_("Fixed fee added to market coin price (e.g., 600000)"),
    )

    market_percent_fee = models.DecimalField(
        _("Percent Fee (%)"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Percentage added to market coin price (e.g., 1 for 1%)"),
    )

    status = models.CharField(
        _("Status"), max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )

    is_active = models.BooleanField(_("Active"), default=True)
    stock = models.PositiveIntegerField(_("Stock"), default=0)

    class Meta:
        verbose_name = _("Coin")
        verbose_name_plural = _("Coins")
        unique_together = ("category", "coin_type")

    def clean(self):
        errors = {}

        # BANK
        if self.category == CoinCategoryEnum.BANK:
            self.weight = None

            if not self.coin_type:
                errors["coin_type"] = _("Coin Type is required for bank coins.")

        # PARSIAN
        elif self.category == CoinCategoryEnum.PARSIAN:
            if self.coin_type:
                errors["coin_type"] = _("Parsian coins do not have a coin type.")

            if self.weight is None:
                errors["weight"] = _("Weight is required for Parsian coins.")

        # MARKET
        elif self.category == CoinCategoryEnum.MARKET:
            if not self.coin_type:
                errors["coin_type"] = _("Coin Type is required for market coins.")

            if self.market_extra_fee is None:
                errors["market_extra_fee"] = _(
                    "Extra fee is required for market coins."
                )

            if self.market_percent_fee is None:
                errors["market_percent_fee"] = _(
                    "Percent fee is required for market coins."
                )

        if errors:
            raise ValidationError(errors)

    @property
    def final_price(self):
        from apps.product.service.price_cache_service import PriceCacheService

        latest = PriceCacheService.get_latest_price()
        if not latest:
            return None

        # BANK
        if self.category == CoinCategoryEnum.BANK:
            mapping = {
                CoinTypeEnum.FULL: latest.full_coin,
                CoinTypeEnum.HALF: latest.half_coin,
                CoinTypeEnum.QUARTER: latest.quarter_coin,
            }
            base_price = mapping.get(self.coin_type)
            if base_price is None:
                return None

            return base_price * Decimal("1.01")

        # PARSIAN
        if self.category == CoinCategoryEnum.PARSIAN:
            if not self.weight:
                return None

            percent_fee = self.market_percent_fee or Decimal("0")
            extra_fee = self.market_extra_fee or Decimal("0")

            return ParsianPricingService.calculate_price(
                weight=self.weight,
                gold_price_per_gram=latest.gold_melted,
                percent_fee=percent_fee,
                extra_fee=extra_fee,
            )

        # MARKET
        if self.category == CoinCategoryEnum.MARKET:
            extra = self.market_extra_fee or Decimal("0")
            percent = self.market_percent_fee or Decimal("0")

            return NormalCoinPricingService.calculate_price(
                internal_gold_17=latest.internal_gold_17,
                coin_type=self.coin_type,
                extra_fee=extra,
                percent_fee=percent,
            )

        return None

    def save(self, *args, **kwargs):
        self.full_clean()

        # جلوگیری از ارور None <= 0
        if self.stock is None:
            self.stock = 0

        # وزن سکه‌های بانکی
        if self.category == CoinCategoryEnum.BANK:
            mapping = {
                CoinTypeEnum.FULL: Decimal("8.133"),
                CoinTypeEnum.HALF: Decimal("4.066"),
                CoinTypeEnum.QUARTER: Decimal("2.033"),
            }
            self.weight = mapping.get(self.coin_type)

        # وزن سکه‌های عادی
        if self.category == CoinCategoryEnum.MARKET:
            mapping = {
                CoinTypeEnum.FULL: Decimal("8.133"),
                CoinTypeEnum.HALF: Decimal("4.066"),
                CoinTypeEnum.QUARTER: Decimal("2.033"),
            }
            self.weight = mapping.get(self.coin_type)

        # وضعیت موجودی
        self.status = (
            ProductStatusEnum.OUT_OF_STOCK
            if self.stock <= 0
            else ProductStatusEnum.AVAILABLE
        )

        super().save(*args, **kwargs)


# TODO : complete final price in phase5
class GoldPriceModel(BaseModel):
    # --- Gold ---
    gold_melted = models.DecimalField(
        _("Gold 18K Price"), max_digits=18, decimal_places=0
    )
    gold_24 = models.DecimalField(_("Gold 24K Price"), max_digits=18, decimal_places=0)
    gold_mozanneh = models.DecimalField(
        _("Muzanneh Price"), max_digits=18, decimal_places=0
    )
    internal_gold_17 = models.DecimalField(
        _("Internal Gold 17K Price"),
        max_digits=18,
        decimal_places=0,
    )
    gold_ounce = models.DecimalField(
        _("Gold Ounce Price"), max_digits=18, decimal_places=0
    )

    # --- Silver ---
    silver_gram = models.DecimalField(
        _("Silver Gram Price (999)"), max_digits=18, decimal_places=0
    )

    # --- Coins ---
    quarter_coin = models.DecimalField(
        _("Quarter Coin Price"), max_digits=18, decimal_places=0
    )
    half_coin = models.DecimalField(
        _("Half Coin Price"), max_digits=18, decimal_places=0
    )
    full_coin = models.DecimalField(
        _("Full Coin Price"), max_digits=18, decimal_places=0
    )

    # --- Currency ---
    usd_price = models.DecimalField(_("USD Price"), max_digits=18, decimal_places=0)

    # --- Meta ---
    effective_at = models.DateTimeField(
        _("Effective At"),
        default=timezone.now,
        db_index=True,
    )
    is_active = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = _("Price Board")
        verbose_name_plural = _("Price Boards")

    def save(self, *args, **kwargs):
        if self.is_active:
            GoldPriceModel.objects.filter(is_active=True).exclude(pk=self.pk).update(
                is_active=False
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Price Board - {self.effective_at}"
