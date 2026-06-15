from apps.product import views
from django.urls import path

app_name = "product"
urlpatterns = [
    path("jewelery/", views.ProductListView.as_view(), name="product_list"),
    path(
        "jewelery/<slug:slug>", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "jewelery/<slug:slug>/buy/", views.ProductBuyView.as_view(), name="product_buy"
    ),
    path("coins/", views.CoinListView.as_view(), name="coin_list"),
]
