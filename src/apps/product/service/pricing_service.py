class PriceService:
    @staticmethod
    def calculate_final_price(
        weight, wage_percent, tax_percent, gold_price, profit_percent
    ):

        # 1) سود + اجرت یک درصدی
        extra = gold_price * ((wage_percent + profit_percent) / 100)

        # 2) قیمت خالص طلا بعد از کم کردن سود و اجرت
        net_gold = gold_price - extra

        # 3) مالیات یک درصدی هر گرم
        tax_per_gram = net_gold * (tax_percent / 100)

        # 4) مالیات کل
        total_tax = tax_per_gram * weight

        # 5) قیمت نهایی هر گرم
        final_per_gram = gold_price + extra + tax_per_gram

        # 6) قیمت نهایی کل
        final = final_per_gram * weight

        return int(final)
