from decimal import ROUND_HALF_UP, Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.order.enums import (
    OrderStatusEnum,
    OrderTypeEnum,
    PaymentMethodEnum,
)
from apps.order.models import (
    OrderItemModel,
    OrderModel,
)
from apps.order.services import InvoiceService
from apps.product.models import GoldPriceModel
from apps.product.service.price_cache_service import PriceCacheService
from apps.wallet import forms, models
from apps.wallet.enums import WalletTransactionTypeEnum
from apps.wallet.services.gold_price_cache_service import MeltRuleCacheService


class MeltedGoldBuyView(LoginRequiredMixin, View):

    MIN_AMOUNT = Decimal("1000000")
    MAX_AMOUNT = Decimal("1000000000")
    STEP_AMOUNT = Decimal("1000000")

    def get(self, request):

        wallet = request.user.wallet

        wallet_balance = Decimal(wallet.balance)

        max_amount = min(
            wallet_balance,
            self.MAX_AMOUNT,
        )

        return render(
            request,
            "wallet/melted_gold_buy.html",
            {
                "wallet_balance": wallet_balance,
                "min_amount": self.MIN_AMOUNT,
                "max_amount": max_amount,
                "step_amount": self.STEP_AMOUNT,
            },
        )

    @transaction.atomic
    def post(self, request):

        amount_raw = request.POST.get("amount")

        if not amount_raw:
            messages.error(
                request,
                _("Please enter an amount"),
            )
            return redirect("wallet:melted_gold_buy")

        try:
            amount = Decimal(amount_raw)
        except (TypeError, ValueError, ArithmeticError):
            messages.error(
                request,
                _("Invalid amount"),
            )
            return redirect("wallet:melted_gold_buy")

        amount = amount.quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )

        # ---------------------------------------------
        # Validate amount
        # ---------------------------------------------

        if amount < self.MIN_AMOUNT:
            messages.error(
                request,
                _("Minimum amount is 1,000,000 Toman"),
            )
            return redirect("wallet:melted_gold_buy")

        if amount > self.MAX_AMOUNT:
            messages.error(
                request,
                _("Maximum purchase amount exceeded"),
            )
            return redirect("wallet:melted_gold_buy")

        if amount % self.STEP_AMOUNT != 0:
            messages.error(
                request,
                _("Invalid amount"),
            )
            return redirect("wallet:melted_gold_buy")

        # ---------------------------------------------
        # Lock wallet
        # ---------------------------------------------

        wallet = models.WalletModel.objects.select_for_update().get(
            pk=request.user.wallet.pk
        )

        if wallet.balance < amount:
            messages.error(
                request,
                _("Your wallet balance is not enough"),
            )
            return redirect("wallet:melted_gold_buy")

        # ---------------------------------------------
        # Get latest gold price
        # ---------------------------------------------

        latest = PriceCacheService.get_latest_price()

        if not latest:
            messages.error(
                request,
                _("Gold price not available"),
            )
            return redirect("wallet:melted_gold_buy")

        # ---------------------------------------------
        # Get active pricing rule
        # ---------------------------------------------

        rule = MeltRuleCacheService.get_latest_rule()

        if not rule:
            messages.error(
                request,
                _("Pricing rule not available"),
            )
            return redirect("wallet:melted_gold_buy")

        # ---------------------------------------------
        # Calculate buy price
        # ---------------------------------------------

        gold_price = Decimal(latest.gold_melted)

        price_per_gram = gold_price * (
            Decimal("1") + Decimal(rule.buy_percent) / Decimal("100")
        )

        price_per_gram = price_per_gram.quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )

        if price_per_gram <= 0:
            messages.error(
                request,
                _("Invalid gold price"),
            )
            return redirect("wallet:melted_gold_buy")

        # ---------------------------------------------
        # Calculate gold amount
        # ---------------------------------------------

        gold_amount = amount / price_per_gram

        gold_amount = gold_amount.quantize(
            Decimal("0.001"),
            rounding=ROUND_HALF_UP,
        )

        if gold_amount <= 0:
            messages.error(
                request,
                _("Invalid gold amount"),
            )
            return redirect("wallet:melted_gold_buy")

        # ---------------------------------------------
        # Create Order
        # ---------------------------------------------

        order = OrderModel.objects.create(
            user=request.user,
            status=OrderStatusEnum.COMPLETED,
            payment_method=PaymentMethodEnum.WALLET,
            order_type=OrderTypeEnum.BUY_MELTED_GOLD,
            total_amount=amount,
            locked_price_at=timezone.now(),
        )

        # ---------------------------------------------
        # Create Order Item
        # ---------------------------------------------

        OrderItemModel.objects.create(
            order=order,
            gold_amount=gold_amount,
            quantity=1,
            unit_price=price_per_gram,
            total_price=amount,
        )

        # ---------------------------------------------
        # Deduct Wallet
        # ---------------------------------------------

        wallet.balance -= amount

        wallet.save(update_fields=["balance"])

        # ---------------------------------------------
        # Wallet Transaction
        # ---------------------------------------------

        models.WalletTransactionModel.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=WalletTransactionTypeEnum.BUY,
            description=_("Buying melted gold"),
            is_success=True,
        )

        # ---------------------------------------------
        # Gold Inventory
        # ---------------------------------------------

        (
            inventory,
            created,
        ) = models.GoldInventoryModel.objects.select_for_update().get_or_create(
            user=request.user,
            defaults={"amount": Decimal("0")},
        )

        inventory.amount += gold_amount

        inventory.save(update_fields=["amount"])

        # ---------------------------------------------
        # Generate Invoice
        # ---------------------------------------------

        invoice = InvoiceService.generate_invoice(order)

        # ---------------------------------------------
        # Mark invoice generated
        # ---------------------------------------------

        order.invoice_generated = True

        order.save(update_fields=["invoice_generated"])

        # ---------------------------------------------
        # Success
        # ---------------------------------------------

        messages.success(
            request,
            _(
                "Purchase successful. "
                "Your melted gold has been added to your inventory."
            ),
        )

        return redirect(
            "wallet:melted_gold_buy",
        )


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
                "dashboard/dashboard.html",
                {
                    "form": form,
                    "inventory": inventory,
                },
            )

        gold_amount = form.cleaned_data["gold_amount"]

        if gold_amount > inventory:
            messages.error(request, _("You don't have enough gold"))
            return redirect("dashboard:dashboard")

        latest_price = GoldPriceModel.objects.filter(is_active=True).last()
        if not latest_price:
            messages.error(request, _("Gold price not available"))
            return redirect("dashboard:dashboard")

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
        return redirect("dashboard:dashboard")
