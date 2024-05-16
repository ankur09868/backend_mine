from django.utils.deprecation import MiddlewareMixin

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.tenant = request.user.tenant
        else:
            request.tenant = None
