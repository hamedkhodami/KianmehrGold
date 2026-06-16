from apps.product.models import CategoryModel, CoinModel, GoldPriceModel, ProductModel
from django.contrib import admin
from django.utils.translation import gettext as _


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
        "tax_percent",
        "stock",
        "status",
        "created_at",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "slug", "description")
    list_filter = ("status", "category", "created_at")
    readonly_fields = ("created_at", "updated_at", "status", "slug")

    fieldsets = (
        (
            _("Product Information"),
            {"fields": ("category", "title", "slug", "image", "description", "stock")},
        ),
        (
            _("Pricing Information"),
            {"fields": ("weight", "wage_percent", "tax_percent", "status")},
        ),
        (_("System Information"), {"fields": ("created_at", "updated_at")}),
    )

    autocomplete_fields = ("category",)
    ordering = ("-created_at",)


@admin.register(CoinModel)
class CoinAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "coin_type",
        "weight",
        "stock",
        "status",
        "is_active",
        "created_at",
    )
    list_display_links = ("id", "coin_type")
    search_fields = ("coin_type",)
    list_filter = ("coin_type", "is_active", "created_at")
    readonly_fields = ("created_at", "updated_at", "status")

    fieldsets = (
        (
            _("Coin Information"),
            {"fields": ("coin_type", "image", "weight", "stock", "is_active")},
        ),
        (_("System Information"), {"fields": ("created_at", "updated_at")}),
    )

    ordering = ("-created_at",)


@admin.register(GoldPriceModel)
class GoldPriceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gold_melted",
        "gold_ounce",
        "gold_mozanneh",
        "quarter_coin",
        "half_coin",
        "full_coin",
        "emami_coin",
        "created_at",
    )
    list_display_links = ("id", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            _("Gold Prices"),
            {
                "fields": (
                    "gold_melted",
                    "gold_ounce",
                    "gold_mozanneh",
                    "quarter_coin",
                    "half_coin",
                    "full_coin",
                    "emami_coin",
                )
            },
        ),
        (_("System Information"), {"fields": ("created_at", "updated_at")}),
    )

    date_hierarchy = "created_at"
    ordering = ("-created_at",)
