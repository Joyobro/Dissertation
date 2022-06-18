
from django.utils.deprecation import MiddlewareMixin

class PutParsingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "DELETE" and request.content_type != "application/json":
            if hasattr(request, '_post'):
                del request._post
                del request._files
            try:
                request.method = "POST"
                request._load_post_and_files()
                request.method = "DELETE"
            except AttributeError as e:
                request.META['REQUEST_METHOD'] = 'POST'
                request._load_post_and_files()
                request.META['REQUEST_METHOD'] = 'DELETE'

            request.PUT = request.POST
