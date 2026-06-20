from apps.account.mixins import AdminRequiredMixin
from apps.order.enums import OrderStatusEnum, OrderTypeEnum
from apps.order.models import OrderModel
from apps.wallet.enums import WalletTransactionTypeEnum
from apps.wallet.models import GoldInventoryModel, WalletTransactionModel
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views import View


class AdminSellMeltedGoldListView(View):
    def get(self, request):

        orders = OrderModel.objects.filter(
            order_type=OrderTypeEnum.SELL_MELTED_GOLD
        ).order_by("-created_at")

        paginator = Paginator(orders, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "order/sell_melted_gold_list.html",
            {
                "page_obj": page_obj,
            },
        )


class AdminApproveSellMeltedGoldView(LoginRequiredMixin, AdminRequiredMixin, View):

    @transaction.atomic
    def post(self, request, order_id):
        order = get_object_or_404(OrderModel, id=order_id)

        if order.status != OrderStatusEnum.PENDING:
            messages.error(request, _("Order is not pending"))
            return redirect("order:admin_sell_list")

        item = order.items.first()
        gold_amount = item.gold_amount
        total_price = item.total_price

        wallet = order.user.wallet
        wallet.balance += total_price
        wallet.save()

        WalletTransactionModel.objects.create(
            wallet=wallet,
            amount=total_price,
            transaction_type=WalletTransactionTypeEnum.SELL,
            description=_("Selling melted gold"),
            is_success=True,
        )

        order.status = OrderStatusEnum.COMPLETED
        order.save()

        messages.success(request, _("Sell request approved"))
        return redirect("order:admin_sell_list")


class AdminRejectSellMeltedGoldView(LoginRequiredMixin, AdminRequiredMixin, View):

    @transaction.atomic
    def post(self, request, order_id):
        order = get_object_or_404(OrderModel, id=order_id)

        if order.status != OrderStatusEnum.PENDING:
            messages.error(request, _("Order is not pending"))
            return redirect("order:admin_sell_list")

        item = order.items.first()
        gold_amount = item.gold_amount

        inventory, created_flag = GoldInventoryModel.objects.get_or_create(
            user=order.user
        )
        inventory.amount += gold_amount
        inventory.save()

        order.status = OrderStatusEnum.CANCELED
        order.save()

        messages.success(request, _("Sell request rejected"))
        return redirect("order:admin_sell_list")


class UserSellMeltedGoldListView(LoginRequiredMixin, View):
    def get(self, request):

        orders = OrderModel.objects.filter(
            user=request.user, order_type=OrderTypeEnum.SELL_MELTED_GOLD
        ).order_by("-created_at")

        paginator = Paginator(orders, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "order/user_sell_melted_gold_list.html",
            {
                "page_obj": page_obj,
            },
        )
