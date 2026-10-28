from django.utils import timezone

from apps.product.models import GoldPriceModel
from apps.product.service.taban_gohar_service import TabanGoharApiService


class PriceBoardBuilder:

    @staticmethod
    def build_from_taban_gohar():
        data = TabanGoharApiService.fetch_latest_price()
        if not data:
            print("[Fail-Safe] API داده نداد → رکورد جدید ساخته نمی‌شود.")
            return None

        try:
            gold_18 = data.get("YekGram18")
            if not gold_18:
                print("[Fail-Safe] داده ناقص → رکورد ساخته نمی‌شود.")
                return None

            board = GoldPriceModel.objects.create(
                gold_melted=gold_18,
                internal_gold_17=int(gold_18 * 4.3318),
                gold_ounce=data.get("OunceTala", 0),
                silver_gram=data.get("GramNoghreh999", 0),
                quarter_coin=(data.get("SekehRob") or 0) * 1000,
                half_coin=(data.get("SekehNim") or 0) * 1000,
                full_coin=(data.get("SekehTamam") or 0) * 1000,
                usd_price=data.get("Dollar", 0),
                effective_at=timezone.now(),
                is_active=True,
            )

            return board

        except Exception as e:
            print("[Fail-Safe] Builder Error:", e)
            return None
