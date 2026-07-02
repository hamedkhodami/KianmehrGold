from django.urls import path

from apps.wallet.views import admin, api, gold, wallet


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
    path("charge/", wallet.WalletChargeView.as_view(), name="charge"),
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
    path("melted-gold/buy/", gold.MeltedGoldBuyView.as_view(), name="melted_gold_buy"),
    path(
        "sell-melted-gold/", gold.SellMeltedGoldView.as_view(), name="sell_melted_gold"
    ),
    # AJAX APIs
    path("api/gold-price/", api.api_get_gold_price, name="api_gold_price"),
    path("api/calc-gold/", api.api_calculate_gold_amount, name="api_calc_gold"),
    path(
        "api/calc-sell-melted-gold/",
        api.api_calc_sell_melted_gold,
        name="api_calc_sell_melted_gold",
    ),
]
