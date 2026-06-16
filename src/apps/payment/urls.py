from apps.payment import views
from django.urls import path

app_name = "payment"

urlpatterns = [
    path("gateway/start/<uuid:payment_id>/", views.gateway_start, name="gateway_start"),
    path("gateway/callback/", views.gateway_callback, name="gateway_callback"),
    # TODO: delete this after get real gateway
    path("fake-gateway/", views.fake_gateway, name="fake_gateway"),
]
