import json
import logging

from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponseNotAllowed

from utils.exception import HttpError

log = logging.getLogger(__name__)


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


class HttpRequest(ASGIRequest):
    def json(self):
        pass
