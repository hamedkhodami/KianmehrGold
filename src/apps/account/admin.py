from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .forms import UserCreationForm
from .models import User, UserBankAccount


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = (
        "id",
        "__str__",
        "first_name",
        "last_name",
        "role",
        "national_code",
        "is_active",
        "is_verified",
    )
    list_display_links = (
        "id",
        "__str__",
    )
    readonly_fields = (
        "created_at",
        "last_login",
    )
    list_filter = ("is_active", "is_admin", "is_verified")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password",
                )
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "role",
                    "national_code",
                )
            },
        ),
        (
            _("Verifications"),
            {"fields": ("is_active", "is_verified", "is_admin", "is_superuser")},
        ),
        (
            _("Dates"),
            {
                "fields": (
                    "last_login",
                    "created_at",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )

    search_fields = (
        "phone_number",
        "first_name",
        "last_name",
    )

    ordering = ("phone_number",)
    date_hierarchy = "created_at"


@admin.register(UserBankAccount)
class UserBankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "bank_name",
        "card_number",
        "iban",
        "created_at",
    )

    list_display_links = (
        "id",
        "user",
    )

    search_fields = (
        "user__phone_number",
        "user__first_name",
        "user__last_name",
        "card_number",
        "iban",
    )

    list_filter = (
        "bank_name",
        "created_at",
    )

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
            _("Bank Information"),
            {
                "fields": (
                    "bank_name",
                    "card_number",
                    "iban",
                )
            },
        ),
        (
            _("Dates"),
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
