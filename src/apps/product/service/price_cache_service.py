from django.core.cache import cache

from apps.product.models import GoldPriceModel


class PriceCacheService:

    @staticmethod
    def get_latest_price():
        key = "latest_price"
        price = cache.get(key)
        if price:
            return price
        price = GoldPriceModel.objects.filter(is_active=True).last()
        cache.set(key, price, 10)
        return price
