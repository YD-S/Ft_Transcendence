import json

from django.core.handlers.asgi import ASGIRequest

from users.models import User


def wrap_funcview(func):
    def wrapper(req, *args, **kwargs):
        request: ASGIRequest | HttpRequest = req
        if not isinstance(request, HttpRequest):
            request = HttpRequest(request)
        return func(request, *args, **kwargs)

    return wrapper


class HttpRequest(ASGIRequest):

    def __init__(self, request: ASGIRequest):
        self.__request = request
        self.content_type = request.headers.get('content-type')

    def __getattr__(self, item):
        if hasattr(self.__request, item):
            return getattr(self.__request, item)
        return super().__getattribute__(item)

    def json(self):
        if self.content_type != 'application/json':
            raise ValueError('Request content type is not application/json')
        if not self.body:
            return {}
        return json.loads(self.body.decode())
