from django.conf import settings
from django.core.cache import cache
import requests


class GoldApiService:
    BASE_URL = "https://api.goldapi.com/v1/latest"

    @classmethod
    def fetch_latest_price(cls):
        cached = cache.get("gold_api_json")
        if cached:
            return cached

        headers = {"Authorization": f"Bearer {settings.GOLD_API_KEY}"}

        try:
            response = requests.get(
                cls.BASE_URL, headers=headers, timeout=settings.GOLD_API_TIMEOUT
            )

            response.raise_for_status()

            data = response.json()
            cache.set("gold_api_json", data, 5)

            return data

        except requests.RequestException:
            return None
