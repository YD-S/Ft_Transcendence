import json

from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponseNotAllowed

from utils.exception import HttpError


class ViewMixin:
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.method not in self.allowed_methods:
                return HttpResponseNotAllowed(self.allowed_methods)
            if kwargs.get('__detail', False):
                del kwargs['__detail']
                pk = kwargs.get("pk")
                del kwargs['pk']
                return self.__pk_path(request, pk, *args, **kwargs)
            return self.__path(request, *args, **kwargs)
        except HttpError as e:
            return e.as_http_response()

    def __pk_path(self, request, pk, *args, **kwargs):
        if request.method == 'GET':
            return self.get(request, pk, *args, **kwargs)
        elif request.method == 'PUT':
            return self.put(request, pk, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.delete(request, pk, *args, **kwargs)
        raise HttpError(405, 'Method not allowed')

    def __path(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.list(request, *args, **kwargs)
        elif request.method == 'POST':
            return self.post(request, *args, **kwargs)
        raise HttpError(405, 'Method not allowed')


class WrappedRequestMixin(ViewMixin):
    def dispatch(self, request, *args, **kwargs):
        request = HttpRequest(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


def wrap_funcview(func):
    def wrapper(req, *args, **kwargs):
        request: ASGIRequest | HttpRequest = req
        if not isinstance(request, HttpRequest):
            request = HttpRequest(request)
        return func(request, *args, **kwargs)

    return wrapper


class HttpRequest(ASGIRequest):

    def __init__(self, request: ASGIRequest, *args, **kwargs):
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
