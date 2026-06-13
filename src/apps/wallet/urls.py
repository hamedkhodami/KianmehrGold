from apps.wallet import views
from django.urls import path

app_name = "wallet"

urlpatterns = [
    path("", views.WalletDashboardView.as_view(), name="wallet_dashboard"),
    path(
        "transactions/<uuid:pk>/",
        views.WalletTransactionDetailView.as_view(),
        name="wallet_transaction_detail",
    ),
    path(
        "withdraw/",
        views.WithdrawRequestCreateView.as_view(),
        name="withdraw_request",
    ),
    path(
        "admin/withdraw-requests/",
        views.AdminWithdrawRequestListView.as_view(),
        name="withdraw_request_list",
    ),
    path(
        "admin/withdraw-requests/<uuid:pk>/",
        views.AdminWithdrawRequestDetailView.as_view(),
        name="admin_withdraw_request_detail",
    ),
    path(
        "table-withdraw-requests/",
        views.WithdrawRequestListView.as_view(),
        name="withdraw_requests",
    ),
]
