from datetime import timedelta

from apps.notification.enums import NotificationEnums
from apps.notification.utils import create_notify_for_admins
from apps.payment.enums import PaymentStatusEnum, PaymentTypeEnum
from apps.payment.models import PaymentModel, WalletChargeModel
from apps.wallet import forms, models
from apps.wallet.models import WithdrawRequestModel
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
)


class WalletDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "wallet/wallet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wallet = self.request.user.wallet

        transactions = wallet.transactions.defer("description").order_by("-created_at")

        paginator = Paginator(transactions, 20)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["wallet"] = wallet
        context["transactions"] = page_obj

        return context


class WalletTransactionDetailView(LoginRequiredMixin, DetailView):
    template_name = "wallet/wallet_transaction_detail.html"
    model = models.WalletTransactionModel
    context_object_name = "transaction"

    def get_queryset(self, **kwargs):
        return self.request.user.wallet.transactions.all()


class WithdrawRequestCreateView(LoginRequiredMixin, CreateView):
    model = models.WithdrawRequestModel
    form_class = forms.WithdrawRequestForm
    template_name = "wallet/withdraw_request.html"
    success_url = reverse_lazy("wallet:wallet_dashboard")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        user = self.request.user
        wallet = models.WalletModel.objects.select_for_update().get(user=user)
        amount = form.cleaned_data["amount"]

        wallet.balance -= amount
        wallet.save()

        form.instance.user = self.request.user
        form.instance.status = models.WithdrawRequestModel.Status.PENDING
        response = super().form_valid(form)

        self.notify_admin(form.instance)

        messages.success(
            self.request, _("Your withdrawal request has been registered.")
        )
        return response

    def notify_admin(self, withdraw_request):
        create_notify_for_admins(
            type=NotificationEnums.ADMIN_ALERT,
            title=_("New withdraw request from %(phone)s")
            % {"phone": withdraw_request.user.phone_number},
        )


class WithdrawRequestListView(LoginRequiredMixin, ListView):
    model = WithdrawRequestModel
    template_name = "wallet/partials/withdraw_requests_table.html"
    context_object_name = "withdraw_requests"
    paginate_by = 20

    def get_queryset(self):
        return WithdrawRequestModel.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


class WalletChargeView(LoginRequiredMixin, FormView):

    template_name = "wallet/charge.html"

    form_class = forms.WalletChargeForm

    @transaction.atomic
    def form_valid(self, form):
        amount = form.cleaned_data["amount"]

        payment = PaymentModel.objects.create(
            user=self.request.user,
            payment_type=PaymentTypeEnum.WALLET_CHARGE,
            amount=amount,
            status=PaymentStatusEnum.PENDING,
            expire_at=timezone.now() + timedelta(minutes=10),
        )

        wallet_charge = WalletChargeModel.objects.create(
            user=self.request.user,
            amount=amount,
            status=PaymentStatusEnum.PENDING,
            payment=payment,
        )

        return redirect(reverse("payment:gateway_start", args=[payment.id]))
