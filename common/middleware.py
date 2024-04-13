from common.request import HttpRequest


class HttpRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        return self.get_response(HttpRequest(request))
