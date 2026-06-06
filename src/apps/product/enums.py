from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ProductStatusEnum(TextChoices):
    AVAILABLE = "available", _("Available")
    OUT_OF_STOCK = "out_of_stock", _("Out Of Stock")
