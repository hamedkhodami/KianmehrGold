from apps.payment.views import callback, gateway
from django.urls import path

app_name = "payment"

urlpatterns = [
    path(
        "gateway/start/<uuid:payment_id>/", gateway.gateway_start, name="gateway_start"
    ),
    path("gateway/callback/", callback.gateway_callback, name="gateway_callback"),
]
