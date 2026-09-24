from decimal import Decimal


class ParsianPricingService:

    @staticmethod
    def calculate_price(
        weight: Decimal,
        gold_price_per_gram: Decimal,
        percent_fee: Decimal,
        extra_fee: Decimal,
    ):
        base = weight * gold_price_per_gram

        with_percent = base * (Decimal("1") + (percent_fee / Decimal("100")))

        final = with_percent + extra_fee

        return final
