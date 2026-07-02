from apps.product.models import GoldPriceModel


def gold_price(request):
    try:
        price = GoldPriceModel.objects.filter(is_active=True).latest("updated_at")
    except GoldPriceModel.DoesNotExist:
        price = None

    return {"gold_price": price}
