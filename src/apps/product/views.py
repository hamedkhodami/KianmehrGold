from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import timedelta
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, View

from apps.order.enums import OrderStatusEnum, OrderTypeEnum, PaymentMethodEnum
from apps.order.models import OrderItemModel, OrderModel
from apps.payment.enums import PaymentStatusEnum, PaymentTypeEnum
from apps.payment.models import PaymentModel
from apps.product.models import CategoryModel, CoinModel, GoldPriceModel, ProductModel


class ProductListView(ListView):
    model = ProductModel
    template_name = "product/product_list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        qs = ProductModel.objects.order_by("-created_at")

        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        status_filter = self.request.GET.get("status")
        if status_filter in ["available", "out_of_stock"]:
            qs = qs.filter(status=status_filter)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = CategoryModel.objects.all()
        context["current_category"] = self.request.GET.get("category")
        context["current_status"] = self.request.GET.get("status")
        context["current_sort"] = self.request.GET.get("sort")
        return context


class ProductDetailView(DetailView):
    model = ProductModel
    template_name = "product/product_detail.html"
    context_object_name = "product"


class ProductBuyView(LoginRequiredMixin, View):

    def get(self, request, id, slug):
        return redirect("product:product_detail", id=id, slug=slug)

    @transaction.atomic
    def post(self, request, id, slug):

        product = ProductModel.objects.select_for_update().get(id=id)

        if product.stock <= 0:

            messages.error(request, _("Product is out of stock."))

            return redirect("product:product_detail", id=id, slug=slug)

        final_price = product.final_price

        if final_price is None:

            messages.error(request, _("Price is not available right now."))

            return redirect("product:product_detail", id=id, slug=slug)

        latest_gold = GoldPriceModel.objects.filter(is_active=True).last()

        order = OrderModel.objects.create(
            user=request.user,
            status=OrderStatusEnum.PENDING,
            payment_method=PaymentMethodEnum.GATEWAY,
            order_type=OrderTypeEnum.BUY_PRODUCT,
            total_amount=final_price,
            expire_at=timezone.now() + timedelta(minutes=5),
            locked_price_at=timezone.now(),
        )

        OrderItemModel.objects.create(
            order=order,
            product=product,
            quantity=1,
            unit_price=final_price,
            total_price=final_price,
        )

        payment = PaymentModel.objects.create(
            user=request.user,
            order=order,
            payment_type=PaymentTypeEnum.ORDER,
            amount=final_price,
            status=PaymentStatusEnum.PENDING,
            expire_at=order.expire_at,
        )

        return redirect(reverse("payment:gateway_start", args=[payment.id]))


class CoinListView(ListView):
    model = CoinModel
    template_name = "product/coin_list.html"
    context_object_name = "coins"
    paginate_by = 20

    def get_queryset(self):
        return CoinModel.objects.filter(is_active=True).order_by("coin_type")


class CoinBuyView(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, coin_uuid):

        coin = CoinModel.objects.select_for_update().get(id=coin_uuid)

        if coin.stock <= 0:

            messages.error(request, _("Coin is out of stock."))

            return redirect("product:coin_list")

        locked_price = coin.final_price

        if locked_price is None:

            messages.error(request, _("Coin price is not available."))

            return redirect("product:coin_list")

        order = OrderModel.objects.create(
            user=request.user,
            status=OrderStatusEnum.PENDING,
            payment_method=PaymentMethodEnum.GATEWAY,
            order_type=OrderTypeEnum.BUY_COIN,
            total_amount=locked_price,
            expire_at=timezone.now() + timedelta(minutes=5),
            locked_price_at=timezone.now(),
        )

        OrderItemModel.objects.create(
            order=order,
            coin=coin,
            quantity=1,
            unit_price=locked_price,
            total_price=locked_price,
        )

        payment = PaymentModel.objects.create(
            user=request.user,
            order=order,
            payment_type=PaymentTypeEnum.ORDER,
            amount=locked_price,
            status=PaymentStatusEnum.PENDING,
            expire_at=order.expire_at,
        )

        return redirect(reverse("payment:gateway_start", args=[payment.id]))
