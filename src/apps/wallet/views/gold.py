from decimal import Decimal

from apps.order.enums import OrderStatusEnum, OrderTypeEnum, PaymentMethodEnum
from apps.order.models import OrderItemModel, OrderModel
from apps.product.models import GoldPriceModel
from apps.wallet import forms, models
from apps.wallet.enums import WalletTransactionTypeEnum
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import View


class MeltedGoldBuyView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "wallet/melted_gold_buy.html")

    @transaction.atomic
    def post(self, request):
        amount = request.POST.get("amount")

        if not amount:
            messages.error(request, _("Please enter an amount"))
            return redirect("wallet:melted_gold_buy")

        try:
            amount = int(amount)
        except:
            messages.error(request, _("Invalid amount"))
            return redirect("wallet:melted_gold_buy")

        if amount < 1_000_000:
            messages.error(request, _("Minimum amount is 1,000,000 Toman"))
            return redirect("wallet:melted_gold_buy")

        wallet = request.user.wallet
        if wallet.balance < amount:
            messages.error(request, _("Your wallet balance is not enough"))
            return redirect("wallet:melted_gold_buy")

        latest = GoldPriceModel.objects.filter(is_active=True).last()
        if not latest:
            messages.error(request, _("Gold price not available"))
            return redirect("wallet:melted_gold_buy")

        gold_amount = amount / latest.gold_melted

        wallet.balance -= amount
        wallet.save()

        models.WalletTransactionModel.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=WalletTransactionTypeEnum.BUY,
            description=_("Buying melted gold"),
            is_success=True,
        )

        inventory, created = models.GoldInventoryModel.objects.get_or_create(
            user=request.user
        )
        inventory.amount += gold_amount
        inventory.save()

        messages.success(request, _("Purchase successful"))
        return redirect("wallet:melted_gold_buy")


class SellMeltedGoldView(LoginRequiredMixin, View):

    def get(self, request):
        form = forms.SellMeltedGoldForm()

        inventory_obj, created_flag = models.GoldInventoryModel.objects.get_or_create(
            user=request.user
        )
        inventory = inventory_obj.amount

        return render(
            request,
            "wallet/sell_melted_gold.html",
            {
                "form": form,
                "inventory": inventory,
            },
        )

    @transaction.atomic
    def post(self, request):
        form = forms.SellMeltedGoldForm(request.POST)

        inventory_obj, created_flag = models.GoldInventoryModel.objects.get_or_create(
            user=request.user
        )
        inventory = inventory_obj.amount

        if not form.is_valid():
            return render(
                request,
                "wallet/sell_melted_gold.html",
                {
                    "form": form,
                    "inventory": inventory,
                },
            )

        gold_amount = form.cleaned_data["gold_amount"]

        if gold_amount > inventory:
            messages.error(request, _("You don't have enough gold"))
            return redirect("wallet:sell_melted_gold")

        latest_price = GoldPriceModel.objects.filter(is_active=True).last()
        if not latest_price:
            messages.error(request, _("Gold price not available"))
            return redirect("wallet:sell_melted_gold")

        unit_price = latest_price.gold_melted  # Decimal
        total_price = (gold_amount * unit_price).quantize(Decimal("1"))

        inventory_obj.amount -= gold_amount
        inventory_obj.save()

        order = OrderModel.objects.create(
            user=request.user,
            order_type=OrderTypeEnum.SELL_MELTED_GOLD,
            status=OrderStatusEnum.PENDING,
            payment_method=PaymentMethodEnum.WALLET,
            total_amount=total_price,
            locked_price_at=timezone.now(),
        )

        OrderItemModel.objects.create(
            order=order,
            gold_amount=gold_amount,
            unit_price=unit_price,
            total_price=total_price,
        )

        messages.success(request, _("Your sell request has been submitted"))
        return redirect("wallet:sell_melted_gold")
