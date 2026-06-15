from apps.payment import views
from django.urls import path

app_name = "payment"

urlpatterns = [
    path("gateway/start/<int:payment_id>/", views.gateway_start, name="gateway_start"),
    path("gateway/callback/", views.gateway_callback, name="gateway_callback"),
]
