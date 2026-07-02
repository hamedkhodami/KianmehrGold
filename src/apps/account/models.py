from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.account.enums import UserRoleEnum
from apps.account.managers import UserManager
from apps.account.validators import (
    validate_card_number,
    validate_iban,
)
from apps.core.models import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    Role = UserRoleEnum

    phone_number = models.CharField(_("Phone number"), max_length=11, unique=True)
    email = models.EmailField(
        _("Email"), max_length=225, null=True, blank=True, unique=True
    )
    first_name = models.CharField(
        _("First name"), max_length=128, null=True, blank=True
    )
    last_name = models.CharField(_("Last name"), max_length=128, null=True, blank=True)
    national_code = models.CharField(
        _("National Code"), max_length=10, blank=True, null=True
    )
    role = models.CharField(
        _("Role"), max_length=128, choices=Role.choices, default=Role.CUSTOMER
    )
    is_active = models.BooleanField(_("Active"), default=True)
    is_admin = models.BooleanField(_("Admin"), default=False)
    is_verified = models.BooleanField(_("Verify"), default=False)
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.phone_number

    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or _("No Name")

    def last_login_within(self, days):
        if self.last_login:
            local_time = timezone.localtime(self.last_login)
            return local_time >= timezone.now() - timedelta(days=days)
        return False

    @property
    def is_staff(self):
        return self.is_superuser or self.is_admin


class UserBankAccount(BaseModel):
    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="bank_accounts",
        verbose_name="User",
    )

    bank_name = models.CharField(_("Bank Name"), max_length=128, blank=True)

    card_number = models.CharField(
        max_length=16,
        validators=[validate_card_number],
        verbose_name="Card Number",
        help_text="16-digit bank card number",
    )

    iban = models.CharField(
        max_length=26,
        validators=[validate_iban],
        verbose_name="IBAN",
        help_text="Iranian Sheba Number",
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name="Default Account",
    )

    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"

    def __str__(self):
        return f"{self.bank_name} " f"({self.card_number[-4:]})"
