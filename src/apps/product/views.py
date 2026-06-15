from apps.payment.enums import PaymentStatusEnum, PaymentTypeEnum
from apps.payment.models import PaymentModel
from apps.product.models import CategoryModel, CoinModel, GoldPriceModel, ProductModel
from apps.product.service.pricing_service import PriceService
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import timedelta
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, View


class ProductListView(LoginRequiredMixin, ListView):
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = ProductModel
    template_name = "product/product_detail.html"
    context_object_name = "product"


class ProductBuyView(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, slug):

        product = ProductModel.objects.select_for_update().get(slug=slug)

        latest_gold = GoldPriceModel.objects.get(is_active=True)

        final_price = PriceService.calculate_final_price(
            weight=product.weight,
            wage_percent=product.wage_percent,
            tax_percent=product.tax_percent,
            gold_price=latest_gold.gold_melted,
        )

        if final_price is None:
            messages.error(request, _("Price is not available right now."))
            return redirect("product:product_detail", slug=slug)

        base = product.weight * latest_gold.gold_melted
        wage_amount = base * (product.wage_percent / 100)
        tax_amount = (base + wage_amount) * (product.tax_percent / 100)

        payment = PaymentModel.objects.create(
            user=request.user,
            payment_type=PaymentTypeEnum.ORDER,  # یا نوع جدید مثلاً PRODUCT_PURCHASE
            amount=final_price,
            status=PaymentStatusEnum.PENDING,
            expire_at=timezone.now() + timedelta(minutes=5),
            product=product,
            locked_gold_price=latest_gold.gold_melted,
            wage_amount=wage_amount,
            tax_amount=tax_amount,
            weight=product.weight,
        )

        return redirect(reverse("payment:gateway_start", args=[payment.id]))


class CoinListView(LoginRequiredMixin, ListView):
    model = CoinModel
    template_name = "product/coin_list.html"
    context_object_name = "coins"
    paginate_by = 20

    def get_queryset(self):
        return CoinModel.objects.filter(is_active=True).order_by("coin_type")
