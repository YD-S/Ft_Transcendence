import json


class HttpRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        def json_f(s):
            if s.headers.get('content-type') != 'application/json':
                raise ValueError('Request content type is not application/json')
            if not s.body:
                return {}
            return json.loads(s.body.decode())

        request.json = json_f.__get__(request)
        return self.get_response(request)
