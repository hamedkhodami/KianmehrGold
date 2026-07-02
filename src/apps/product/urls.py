from django.urls import path

from apps.product import views


app_name = "product"
urlpatterns = [
    path("jewelery/", views.ProductListView.as_view(), name="product_list"),
    path(
        "jewelery/<uuid:id>/<path:slug>/buy/",
        views.ProductBuyView.as_view(),
        name="product_buy",
    ),
    path(
        "jewelery/<uuid:id>/<path:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("coins/", views.CoinListView.as_view(), name="coin_list"),
    path("coins/<uuid:coin_uuid>/buy", views.CoinBuyView.as_view(), name="coin_buy"),
]
