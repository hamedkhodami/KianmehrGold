from apps.wallet.models import (
    CoinInventoryModel,
    GoldInventoryModel,
    WalletModel,
    WalletTransactionModel,
    WithdrawRequestModel,
)
from django.contrib import admin
from django.utils.translation import gettext as _


@admin.register(WalletModel)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "balance",
    )

    list_display_links = (
        "id",
        "user",
    )

    search_fields = (
        "user__phone_number",
        "user__first_name",
        "user__last_name",
    )

    list_filter = ("created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("User Information"),
            {"fields": ("user",)},
        ),
        (
            _("Balance Information"),
            {"fields": ("balance",)},
        ),
    )

    autocomplete_fields = ("user",)

    ordering = ("-created_at",)

    date_hierarchy = "created_at"


@admin.register(WalletTransactionModel)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "wallet",
        "amount",
        "transaction_type",
        "description",
        "is_success",
    )

    list_display_links = (
        "id",
        "wallet",
    )

    list_filter = ("created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("Wallet Information"),
            {"fields": ("wallet",)},
        ),
        (
            _("Other Information"),
            {
                "fields": (
                    "amount",
                    "transaction_type",
                    "description",
                    "is_success",
                )
            },
        ),
    )

    autocomplete_fields = ("wallet",)

    ordering = ("-created_at",)

    date_hierarchy = "created_at"


@admin.register(WithdrawRequestModel)
class WithdrawRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "admin_note",
    )

    list_display_links = (
        "id",
        "user",
    )

    list_filter = ("created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("User Information"),
            {"fields": ("user",)},
        ),
        (
            _("Other Information"),
            {
                "fields": (
                    "amount",
                    "status",
                    "admin_note",
                )
            },
        ),
    )

    autocomplete_fields = ("user",)

    ordering = ("-created_at",)

    date_hierarchy = "created_at"


@admin.register(CoinInventoryModel)
class CoinInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "coin_type",
        "amount",
    )

    list_display_links = (
        "id",
        "user",
    )

    list_filter = ("created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("User Information"),
            {"fields": ("user",)},
        ),
        (
            _("Other Information"),
            {
                "fields": (
                    "coin_type",
                    "amount",
                )
            },
        ),
    )

    autocomplete_fields = ("user",)

    ordering = ("-created_at",)

    date_hierarchy = "created_at"


@admin.register(GoldInventoryModel)
class GoldInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
    )

    list_display_links = (
        "id",
        "user",
    )

    list_filter = ("created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("User Information"),
            {"fields": ("user",)},
        ),
        (
            _("Other Information"),
            {"fields": ("amount",)},
        ),
    )

    autocomplete_fields = ("user",)

    ordering = ("-created_at",)

    date_hierarchy = "created_at"
