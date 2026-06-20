from apps.order import views
from django.urls import path

app_name = "order"

urlpatterns = [
    path(
        "admin/sell-melted-gold/",
        views.AdminSellMeltedGoldListView.as_view(),
        name="admin_sell_list",
    ),
    path(
        "admin/sell-melted-gold/<uuid:order_id>/approve/",
        views.AdminApproveSellMeltedGoldView.as_view(),
        name="admin_sell_approve",
    ),
    path(
        "admin/sell-melted-gold/<uuid:order_id>/reject/",
        views.AdminRejectSellMeltedGoldView.as_view(),
        name="admin_sell_reject",
    ),
    path(
        "my/sell-melted-gold/",
        views.UserSellMeltedGoldListView.as_view(),
        name="user_sell_list",
    ),
]
