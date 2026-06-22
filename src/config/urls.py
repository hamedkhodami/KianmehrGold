from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("apps.public.urls", namespace="public")),
    path("accounts/", include("apps.account.urls", namespace="account")),
    path("wallet/", include("apps.wallet.urls", namespace="wallet")),
    path("product/", include("apps.product.urls", namespace="product")),
    path("payment/", include("apps.payment.urls", namespace="payment")),
    path("order/", include("apps.order.urls", namespace="order")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
]

# --- Static files ---
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# --- Media files ---
if settings.DEBUG or getattr(settings, "ENABLE_MEDIA_SERVE_IN_LOCAL", False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
