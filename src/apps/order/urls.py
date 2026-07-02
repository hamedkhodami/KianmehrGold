from django.urls import path

from apps.order import views


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
    path("invoices/", views.UserInvoiceListView.as_view(), name="invoice_list"),
    path(
        "invoices/<uuid:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"
    ),
    path("invoices/<uuid:pk>/pdf/", views.InvoicePDFView.as_view(), name="invoice_pdf"),
]
