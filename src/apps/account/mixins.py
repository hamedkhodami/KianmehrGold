from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class LogoutRequiredMixin:
    """Anonymous users access only"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    def handle_no_permission(self):
        raise PermissionDenied(_("You do not have permission to access this page."))
