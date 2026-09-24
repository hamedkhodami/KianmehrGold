from django.urls import path

from apps.notification.views import UserNotificationListView


app_name = "notification"

urlpatterns = [
    path("my/", UserNotificationListView.as_view(), name="user_notifications"),
]
