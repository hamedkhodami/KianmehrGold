from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.generic import ListView, View

from apps.account.mixins import AdminRequiredMixin
from apps.notification.enums import NotificationEnums
from apps.notification.models import Notification
from apps.wallet import models
from apps.wallet.models import WithdrawRequestModel


class AdminWithdrawRequestListView(AdminRequiredMixin, ListView):
    model = WithdrawRequestModel
    template_name = "wallet/admin/withdraw_request_list.html"
    context_object_name = "requests"
    paginate_by = 20

    def get_queryset(self):
        return WithdrawRequestModel.objects.select_related("user").order_by(
            "-created_at"
        )


class AdminWithdrawRequestDetailView(AdminRequiredMixin, View):
    template_name = "wallet/admin/withdraw_request_detail.html"

    def get(self, request, pk):
        withdraw_request = get_object_or_404(WithdrawRequestModel, pk=pk)

        if withdraw_request.status != WithdrawRequestModel.Status.PENDING:
            messages.error(request, _("This request is already processed."))
            return redirect("wallet:withdraw_request_list")

        bank_account = (
            withdraw_request.user.bank_accounts.filter(is_default=True).first()
            or withdraw_request.user.bank_accounts.first()
        )

        context = {
            "withdraw_request": withdraw_request,
            "bank_account": bank_account,
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, pk):
        withdraw_request = WithdrawRequestModel.objects.select_for_update().get(
            pk=pk, status=WithdrawRequestModel.Status.PENDING
        )
        user = withdraw_request.user
        wallet = models.WalletModel.objects.select_for_update().get(user=user)
        amount = withdraw_request.amount

        admin_note = request.POST.get("admin_note", "")
        action = request.POST.get("action")

        if action == "approve":

            models.WalletTransactionModel.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type=models.WalletTransactionModel.Type.WITHDRAW,
                description=_("Withdraw approved by admin"),
                is_success=True,
            )

            withdraw_request.status = WithdrawRequestModel.Status.PAID
            withdraw_request.admin_note = admin_note
            withdraw_request.save()

            Notification.objects.create(
                type=NotificationEnums.WALLET_TRANSACTION,
                to_user=withdraw_request.user,
                title=_("Withdraw approved by admin"),
                kwargs={"amount": str(amount), "status": "approved"},
            )

            messages.success(request, _("Withdraw request approved."))

        elif action == "reject":
            wallet.balance += amount
            wallet.save()

            models.WalletTransactionModel.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type=models.WalletTransactionModel.Type.DEPOSIT,  # یا REFUND
                description=_("Withdraw request rejected, amount refunded"),
                is_success=True,
            )

            withdraw_request.status = WithdrawRequestModel.Status.REJECTED
            withdraw_request.admin_note = admin_note
            withdraw_request.save()

            Notification.objects.create(
                type=NotificationEnums.WALLET_TRANSACTION,
                to_user=withdraw_request.user,
                title=_("Withdraw rejected by admin"),
                kwargs={"amount": str(amount), "status": "rejected"},
            )
            messages.error(request, _("Withdraw request rejected."))

        else:
            messages.error(request, _("Invalid action."))

        return redirect("dashboard:dashboard")
