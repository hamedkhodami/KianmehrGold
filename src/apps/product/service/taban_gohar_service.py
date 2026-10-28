from django.conf import settings
from django.core.cache import cache
import requests


class TabanGoharApiService:
    BASE_URL = "https://webservice.tgnsrv.ir/Pr/Get"

    @classmethod
    def fetch_latest_price(cls):
        cached = cache.get("taban_gohar_json")
        if cached:
            return cached

        url = f"{cls.BASE_URL}/{settings.TABAN_GOHAR_USERNAME}/{settings.TABAN_GOHAR_PASSWORD}"

        try:
            response = requests.get(url, timeout=settings.TABAN_GOHAR_TIMEOUT)
            response.raise_for_status()

            data = response.json()

            # Fail-Safe: اگر API ارور داد
            if not isinstance(data, dict):
                return None

            if data.get("Error"):
                return None

            # Fail-Safe: اگر کلیدهای اصلی نبودند
            required_keys = ["YekGram18", "SekehTamam", "Dollar"]
            if any(key not in data for key in required_keys):
                return None

            cache.set("taban_gohar_json", data, settings.TABAN_GOHAR_CACHE_SECONDS)
            return data

        except:
            return None
