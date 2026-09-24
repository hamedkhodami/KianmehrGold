from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class NotificationTypeEnum(TextChoices):
    MOBILE_VERIFICATION_CODE = "mobile-verification-code", _("Mobile Verification Code")
    WALLET_TRANSACTION = "wallet-transaction", _("Wallet Transaction")
    ADMIN_ALERT = "admin-alert", _("Admin Alert")
    SYSTEM = "system", _("System")


class NotificationChannelEnum(TextChoices):
    SMS = "sms", _("SMS")
    IN_APP = "in-app", _("In App")
    EMAIL = "email", _("Email")
