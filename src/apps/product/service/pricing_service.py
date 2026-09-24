class PriceService:
    @staticmethod
    def calculate_final_price(
        weight,
        wage_percent,
        tax_percent,
        gold_price,
        profit_percent,
    ):
        base = weight * gold_price

        wage = base * (wage_percent / 100)

        profit = (base + wage) * (profit_percent / 100)

        tax_base = base + wage + profit
        tax = tax_base * (tax_percent / 100)

        final = base + wage + profit + tax

        return int(final)
