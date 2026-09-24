from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from apps.notification.models import Notification


class UserNotificationListView(LoginRequiredMixin, View):
    def get(self, request):
        notifications = Notification.objects.filter(to_user=request.user).order_by(
            "-created_at"
        )

        paginator = Paginator(notifications, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "notification/user_notifications.html",
            {
                "notifications": page_obj.object_list,
                "page_obj": page_obj,
            },
        )
