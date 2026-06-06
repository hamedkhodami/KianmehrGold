from apps.payment.models import PaymentModel, WalletChargeModel
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "payment_type",
        "amount",
        "status",
        "authority",
        "ref_id",
        "created_at",
    )

    list_display_links = ("id", "user")

    list_filter = (
        "payment_type",
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__phone_number",
        "authority",
        "ref_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "authority",
        "ref_id",
    )

    fieldsets = (
        (
            _("Payment Information"),
            {
                "fields": (
                    "user",
                    "payment_type",
                    "order",
                    "amount",
                    "status",
                )
            },
        ),
        (
            _("Gateway Information"),
            {
                "fields": (
                    "authority",
                    "ref_id",
                )
            },
        ),
        (
            _("System Information"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    autocomplete_fields = ("user", "order")

    ordering = ("-created_at",)

    date_hierarchy = "created_at"


@admin.register(WalletChargeModel)
class WalletChargeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "status",
        "payment",
        "created_at",
    )

    list_display_links = ("id", "user")

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__phone_number",
        "payment__ref_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("Charge Information"),
            {
                "fields": (
                    "user",
                    "amount",
                    "status",
                    "payment",
                )
            },
        ),
        (
            _("System Information"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    autocomplete_fields = ("user", "payment")

    ordering = ("-created_at",)

    date_hierarchy = "created_at"
