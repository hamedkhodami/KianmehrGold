from apps.order.models import InvoiceModel, OrderItemModel, OrderModel
from django.contrib import admin
from django.utils.translation import gettext as _


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "order_type",
        "payment_method",
        "status",
        "total_amount",
        "created_at",
    )

    list_display_links = ("id", "user")

    list_filter = (
        "status",
        "payment_method",
        "order_type",
        "created_at",
    )

    search_fields = (
        "id",
        "user__phone_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("Order Information"),
            {
                "fields": (
                    "user",
                    "order_type",
                    "payment_method",
                    "status",
                    "total_amount",
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

    autocomplete_fields = ("user",)

    ordering = ("-created_at",)

    date_hierarchy = "created_at"


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "coin",
        "gold_amount",
        "quantity",
        "unit_price",
        "total_price",
        "created_at",
    )

    list_display_links = ("id", "order")

    list_filter = (
        "created_at",
        "product",
        "coin",
    )

    search_fields = (
        "order__id",
        "product__title",
        "coin__coin_type",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("Order Item Information"),
            {
                "fields": (
                    "order",
                    "product",
                    "coin",
                    "gold_amount",
                    "quantity",
                    "unit_price",
                    "total_price",
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

    autocomplete_fields = ("order", "product", "coin")

    ordering = ("-created_at",)

    date_hierarchy = "created_at"


@admin.register(InvoiceModel)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice_number",
        "order",
        "amount",
        "tax_amount",
        "wage_amount",
        "is_paid",
        "paid_at",
        "created_at",
    )

    list_display_links = ("id", "invoice_number")

    list_filter = (
        "is_paid",
        "created_at",
    )

    search_fields = (
        "invoice_number",
        "order__id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "paid_at",
    )

    fieldsets = (
        (
            _("Invoice Information"),
            {
                "fields": (
                    "invoice_number",
                    "order",
                    "amount",
                    "tax_amount",
                    "wage_amount",
                    "is_paid",
                    "paid_at",
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

    autocomplete_fields = ("order",)

    ordering = ("-created_at",)

    date_hierarchy = "created_at"
