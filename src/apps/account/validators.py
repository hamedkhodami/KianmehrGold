import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_card_number(value: str) -> None:
    """
    Validate Iranian bank card number.
    """
    value = value.replace("-", "").replace(" ", "")
    if not value.isdigit():
        raise ValidationError(_("Card number must contain only digits."))

    if len(value) != 16:
        raise ValidationError(_("Card number must contain exactly 16 digits."))


def validate_iban(value: str) -> None:

    value = value.upper().replace(" ", "")

    pattern = r"^IR\d{24}$"

    if not re.match(pattern, value):
        raise ValidationError("Invalid Iranian IBAN format.")
