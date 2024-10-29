import json


class HttpRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        def json_f(self):
            if self.__request.headers.get('content-type') != 'application/json':
                raise ValueError('Request content type is not application/json')
            if not self.body:
                return {}
            return json.loads(self.body.decode())

        request.json = json_f
        return self.get_response(request)
