from django.utils import timezone

from apps.product.service.price_board_service import PriceBoardBuilder


def update_price_board():

    price_board = PriceBoardBuilder.build_from_taban_gohar()

    if price_board:
        print(f"[{timezone.now()}] Price board updated successfully.")
    else:
        print(f"[{timezone.now()}] Failed to fetch price from Taban Gohar.")
