class PriceService:
    @staticmethod
    def calculate_final_price(weight, wage_percent, tax_percent, gold_price):
        base = weight * gold_price
        wage = base * (wage_percent / 100)
        tax = (base + wage) * (tax_percent / 100)
        return int(base + wage + tax)
