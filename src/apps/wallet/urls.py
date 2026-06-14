from apps.wallet.views import admin, wallet
from django.urls import path

app_name = "wallet"

urlpatterns = [
    path("", wallet.WalletDashboardView.as_view(), name="wallet_dashboard"),
    path(
        "transactions/<uuid:pk>/",
        wallet.WalletTransactionDetailView.as_view(),
        name="wallet_transaction_detail",
    ),
    path(
        "withdraw/",
        wallet.WithdrawRequestCreateView.as_view(),
        name="withdraw_request",
    ),
    path(
        "table-withdraw-requests/",
        wallet.WithdrawRequestListView.as_view(),
        name="withdraw_requests",
    ),
    path(
        "admin/withdraw-requests/",
        admin.AdminWithdrawRequestListView.as_view(),
        name="withdraw_request_list",
    ),
    path(
        "admin/withdraw-requests/<uuid:pk>/",
        admin.AdminWithdrawRequestDetailView.as_view(),
        name="admin_withdraw_request_detail",
    ),
]
