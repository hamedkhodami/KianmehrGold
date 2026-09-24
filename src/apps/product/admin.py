from django.contrib import admin
from django.utils.translation import gettext as _

from apps.product.forms import CoinModelForm
from apps.product.models import (
    CategoryModel,
    CoinModel,
    GoldPriceModel,
    ProductModel,
)


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "icon", "created_at")
    list_display_links = ("id", "title")
    search_fields = ("title", "slug")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at", "slug")

    fieldsets = (
        (
            _("Category Information"),
            {"fields": ("title", "slug", "description", "icon")},
        ),
        (_("System Information"), {"fields": ("created_at", "updated_at")}),
    )

    ordering = ("-created_at",)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "weight",
        "slug",
        "wage_percent",
        "profit_percent",
        "tax_percent",
        "status",
        "created_at",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "slug", "description", "id")
    list_filter = ("status", "category", "created_at")
    readonly_fields = ("created_at", "updated_at", "status", "slug")

    fieldsets = (
        (
            _("Product Information"),
            {"fields": ("category", "title", "slug", "image", "description", "stock")},
        ),
        (
            _("Pricing Information"),
            {
                "fields": (
                    "weight",
                    "wage_percent",
                    "profit_percent",
                    "tax_percent",
                    "status",
                )
            },
        ),
        (_("System Information"), {"fields": ("created_at", "updated_at")}),
    )

    autocomplete_fields = ("category",)
    ordering = ("-created_at",)


@admin.register(CoinModel)
class CoinAdmin(admin.ModelAdmin):
    form = CoinModelForm

    list_display = (
        "id",
        "category",
        "coin_type",
        "weight",
        "market_extra_fee",
        "market_percent_fee",
        "status",
        "is_active",
        "stock",
        "created_at",
    )

    search_fields = (
        "category",
        "coin_type",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "status",
    )

    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "category",
                    "image",
                    "stock",
                    "status",
                    "is_active",
                ),
            },
        ),
        (
            "Coin Type (Bank & Normal Coins)",
            {
                "fields": ("coin_type",),
            },
        ),
        (
            "Weight",
            {
                "fields": ("weight",),
            },
        ),
        (
            "Pricing (Parsian & Normal Coins)",
            {
                "fields": (
                    "market_extra_fee",
                    "market_percent_fee",
                ),
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    class Media:
        js = ("public/js/admin.js",)


@admin.register(GoldPriceModel)
class GoldPriceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gold_melted",
        "internal_gold_17",
        "gold_mozanneh",
        "gold_ounce",
        "silver_gram",
        "usd_price",
        "is_active",
        "effective_at",
        "created_at",
    )

    list_filter = (
        "is_active",
        "effective_at",
        "created_at",
    )

    search_fields = (
        "id",
        "effective_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("Gold Prices"),
            {
                "fields": (
                    "gold_melted",
                    "gold_24",
                    "gold_mozanneh",
                    "internal_gold_17",
                    "gold_ounce",
                )
            },
        ),
        (
            _("Silver Prices"),
            {"fields": ("silver_gram",)},
        ),
        (
            _("Coin Prices"),
            {
                "fields": (
                    "quarter_coin",
                    "half_coin",
                    "full_coin",
                )
            },
        ),
        (
            _("Currency Prices"),
            {"fields": ("usd_price",)},
        ),
        (
            _("Meta Information"),
            {
                "fields": (
                    "is_active",
                    "effective_at",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    ordering = ("-effective_at", "-created_at")
