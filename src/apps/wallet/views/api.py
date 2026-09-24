from decimal import Decimal

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.product.service.price_cache_service import PriceCacheService
from apps.wallet.services.gold_price_cache_service import MeltRuleCacheService


def api_get_gold_price(request):
    latest = PriceCacheService.get_latest_price()
    if not latest:
        return JsonResponse(
            {"success": False, "error": _("Price not available")}, status=400
        )

    return JsonResponse({"success": True, "gold_price": int(latest.gold_melted)})


@require_POST
def api_calc_buy_melted_gold(request):
    try:
        amount = Decimal(request.POST.get("amount"))
    except (TypeError, ValueError, ArithmeticError):
        return JsonResponse(
            {
                "success": False,
                "error": _("Invalid amount"),
            }
        )

    if amount < Decimal("1000000"):
        return JsonResponse(
            {
                "success": False,
                "error": _("Minimum amount is 1,000,000 Toman"),
            }
        )

    latest = PriceCacheService.get_latest_price()

    if not latest:
        return JsonResponse(
            {
                "success": False,
                "error": _("Gold price not available"),
            }
        )

    rule = MeltRuleCacheService.get_latest_rule()

    if not rule:
        return JsonResponse(
            {
                "success": False,
                "error": _("Pricing rule not available"),
            }
        )

    gold_price = Decimal(latest.gold_melted)

    price_per_gram = gold_price * (Decimal("1") + rule.buy_percent / Decimal("100"))

    price_per_gram = price_per_gram.quantize(Decimal("1"))

    gold_amount = amount / price_per_gram

    gold_amount = gold_amount.quantize(Decimal("0.001"))

    return JsonResponse(
        {
            "success": True,
            "gold_amount": str(gold_amount),
            "price_per_gram": int(price_per_gram),
            "total_amount": int(amount),
            "buy_percent": str(rule.buy_percent),
        }
    )


@require_POST
def api_calc_sell_melted_gold(request):
    try:
        gold_amount = Decimal(request.POST.get("gold_amount"))
    except (TypeError, ValueError, ArithmeticError):
        return JsonResponse(
            {
                "success": False,
                "error": _("Invalid amount"),
            }
        )

    if gold_amount <= 0:
        return JsonResponse(
            {
                "success": False,
                "error": _("Invalid amount"),
            }
        )

    latest = PriceCacheService.get_latest_price()

    if not latest:
        return JsonResponse(
            {
                "success": False,
                "error": _("Gold price not available"),
            }
        )

    rule = MeltRuleCacheService.get_latest_rule()

    if not rule:
        return JsonResponse(
            {
                "success": False,
                "error": _("Pricing rule not available"),
            }
        )

    gold_price = Decimal(latest.gold_melted)

    price_per_gram = gold_price * (Decimal("1") - rule.sell_percent / Decimal("100"))

    price_per_gram = price_per_gram.quantize(Decimal("1"))

    total_price = gold_amount * price_per_gram

    return JsonResponse(
        {
            "success": True,
            "unit_price": int(price_per_gram),
            "total_price": int(total_price),
        }
    )
