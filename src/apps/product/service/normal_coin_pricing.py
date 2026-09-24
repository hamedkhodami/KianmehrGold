from decimal import Decimal


class NormalCoinPricingService:

    @staticmethod
    def calculate_price(
        internal_gold_17: Decimal,
        coin_type: str,
        extra_fee: Decimal,
        percent_fee: Decimal,
    ):
        n = internal_gold_17 * Decimal("2.253")

        mapping = {
            "full": Decimal("1"),
            "half": Decimal("0.5"),
            "quarter": Decimal("0.25"),
        }

        base = n * mapping.get(coin_type, Decimal("1"))

        percent_amount = (base * percent_fee) / Decimal("100")

        final_price = base + percent_amount + extra_fee

        return final_price
