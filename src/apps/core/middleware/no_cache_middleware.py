from django.utils.deprecation import MiddlewareMixin


class NoCacheForAdminMiddleware(MiddlewareMixin):

    def process_response(self, request, response):

        if request.path.startswith("/admin/") or request.path.startswith("/dashboard/"):
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"

        return response
