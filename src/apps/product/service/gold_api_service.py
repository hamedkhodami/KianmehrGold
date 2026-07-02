from django.conf import settings
import requests


class GoldApiService:
    BASE_URL = "https://api.goldapi.com/v1/latest"

    @classmethod
    def fetch_latest_price(cls):

        headers = {"Authorization": f"Bearer {settings.GOLD_API_KEY}"}

        try:
            response = requests.get(cls.BASE_URL, headers=headers, timeout=5)

            response.raise_for_status()

            return response.json()

        except requests.RequestException:
            return None
