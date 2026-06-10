from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class NotificationEnums(TextChoices):
    MOBILE_VERIFICATION_CODE = "mobile-verification-code", _("Mobile Verification Code")
    ORDER_STATUS = "order-status", _("Order Status")
    WALLET_TRANSACTION = "wallet-transaction", _("Wallet Transaction")
    ADMIN_ALERT = "admin-alert", _("Admin Alert")
