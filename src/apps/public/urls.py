from django.urls import path

from . import views


app_name = "public"

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("about/", views.AboutUsView.as_view(), name="about_us"),
    path("articles/", views.ArticleListView.as_view(), name="article_list"),
    path(
        "articles/<uuid:id>/<path:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
]
