from django.shortcuts import redirect


class LogoutRequiredMixin:
    """Anonymous users access only"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)
