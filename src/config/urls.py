from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("accounts/", include("apps.account.urls", namespace="account")),
    path("", include("apps.public.urls", namespace="public")),
]
