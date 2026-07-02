from decimal import Decimal

from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from apps.product.models import GoldPriceModel


def api_get_gold_price(request):
    latest = GoldPriceModel.objects.filter(is_active=True).last()
    if not latest:
        return JsonResponse(
            {"success": False, "error": "Price not available"}, status=400
        )

    return JsonResponse({"success": True, "gold_price": int(latest.gold_melted)})


@require_POST
def api_calculate_gold_amount(request):
    try:
        amount = int(request.POST.get("amount"))
    except:
        return JsonResponse({"success": False, "error": _("Invalid amount")})

    latest = GoldPriceModel.objects.filter(is_active=True).last()
    if not latest:
        return JsonResponse({"success": False, "error": _("Gold price not available")})

    gold_price = latest.gold_melted
    gold_amount = amount / gold_price

    return JsonResponse({"success": True, "gold_amount": round(gold_amount, 3)})


@require_POST
def api_calc_sell_melted_gold(request):
    try:
        gold_amount = Decimal(request.POST.get("gold_amount"))
    except:
        return JsonResponse({"success": False, "error": _("Invalid amount")})

    latest = GoldPriceModel.objects.filter(is_active=True).last()
    if not latest:
        return JsonResponse({"success": False, "error": _("Gold price not available")})

    unit_price = latest.gold_melted  # already Decimal
    total_price = gold_amount * unit_price  # now works

    return JsonResponse(
        {
            "success": True,
            "unit_price": int(unit_price),
            "total_price": int(total_price),
        }
    )
