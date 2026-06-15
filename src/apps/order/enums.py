from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class OrderStatusEnum(TextChoices):
    PENDING = "pending", _("Pending")
    PAID = "paid", _("Paid")
    CANCELED = "canceled", _("Canceled")
    COMPLETED = "completed", _("Completed")


class PaymentMethodEnum(TextChoices):
    WALLET = "wallet", _("Wallet")
    GATEWAY = "gateway", _("Gateway")
    CASH = "cash", _("Cash Payment")


class OrderTypeEnum(TextChoices):
    BUY_PRODUCT = "buy_product", _("Buy Product")
    SELL_PRODUCT = "sell_product", _("Sell Product")
    BUY_COIN = "buy_coin", _("Buy Coin")
    SELL_COIN = "sell_coin", _("Sell Coin")
    BUY_MELTED_GOLD = "buy_melted_gold", _("Buy Melted Gold")
    SELL_MELTED_GOLD = "sell_melted_gold", _("Sell Melted Gold")
