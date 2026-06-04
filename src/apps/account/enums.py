from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class UserRoleEnum(TextChoices):
    ADMIN = "admin", _("Admin")
    CUSTOMER = "customer", _("Customer")
