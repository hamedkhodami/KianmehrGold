from apps.product.models import GoldPriceModel
from apps.product.service.gold_api_service import GoldApiService


def update_gold_prices():

    data = GoldApiService.fetch_latest_price()

    if not data:
        return

    GoldPriceModel.objects.update_or_create(
        is_active=True,
        defaults={
            "gold_melted": data["gold_melted"],
            "gold_ounce": data["gold_ounce"],
            "gold_mozanneh": data["gold_mozanneh"],
            "quarter_coin": data["quarter_coin"],
            "half_coin": data["half_coin"],
            "full_coin": data["full_coin"],
            "emami_coin": data["emami_coin"],
        },
    )
