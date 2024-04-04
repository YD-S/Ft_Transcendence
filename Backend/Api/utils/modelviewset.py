import json
from functools import reduce
from typing import Type, Callable, List

from django.db import models
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.http import require_http_methods

from common.request import HttpRequest, wrap_funcview
from utils.exception import HttpError, NotFoundError
from utils.modelserializer import ModelSerializer


class ModelViewSet:
    __methods = []

    def __init__(self, m: Type[models.Model], s: Type[ModelSerializer]):
        self.decorators: list[Callable] = [
            wrap_funcview
        ]
        self.model: Type[models.Model] = m
        self.serializer: Type[ModelSerializer] = s

    @classmethod
    def view(cls, url: str, methods: List[str]):
        def decorator(func: Callable):
            cls.__methods.append({
                'url': url,
                'methods': methods,
                'func': func
            })

            return func

        return decorator

    def get(self, request: HttpRequest, pk):
        instance = self.get_instance(pk)
        serializer = self.serializer(instance=instance)
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(serializer.data))

    def list(self, request: HttpRequest):
        qs = self.model.objects.all()
        data = []
        for instance in qs:
            serializer = self.serializer(instance=instance)
            data.append(serializer.data)
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(data))

    def post(self, request: HttpRequest):
        serializer = self.serializer(data=request.json())
        instance = serializer.save()
        serializer = self.serializer(instance=instance)
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(serializer.data))

    def put(self, request: HttpRequest, pk: int):
        instance = self.get_instance(pk)
        data = request.json()
        serializer = self.serializer(instance=instance, data=data)
        serializer.save()
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(serializer.data))

    def delete(self, request: HttpRequest, pk: int):
        instance = self.get_instance(pk)
        serializer = self.serializer(instance=instance)
        instance.delete()
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(serializer.data))

    def get_instance(self, pk: int):
        qs = self.model.objects.filter(pk=pk)
        if not qs.exists():
            raise NotFoundError()
        return qs.first()

    @staticmethod
    def _endpoint(method: Callable, request: HttpRequest, *args, **kwargs):
        try:
            return method(request, *args, **kwargs)
        except HttpError as e:
            return e.as_http_response()

    def as_urls(self):
        return [
            path('',
                 reduce(
                     lambda x, y: y(x),
                     self.decorators,
                     require_http_methods(["GET", "POST"])(lambda req: self.__root_path(req)))
                 ,
                 name='list_create'),
            path('<int:pk>/',
                 reduce(
                     lambda x, y: y(x),
                     self.decorators,
                     require_http_methods(["GET", "PUT", "DELETE"])(lambda req, pk: self.__pk_path(req, pk))
                 ),
                 name='retrieve_update_delete'),
        ] + [
            path(method['url'],
                 reduce(
                     lambda x, y: y(x),
                     self.decorators,
                     require_http_methods(method['methods'])(method['func'])
                 ),
                 name=f'{method["func"].__name__}')
            for method in self.__methods
        ]

    def __root_path(self, request: HttpRequest):
        if request.method == 'GET':
            return self._endpoint(self.list, request)
        elif request.method == 'POST':
            return self._endpoint(self.list, request)
        raise HttpError(405, 'Method not allowed')

    def __pk_path(self, request: HttpRequest, pk: int):
        if request.method == 'GET':
            return self._endpoint(self.get, request, pk)
        elif request.method == 'PUT':
            return self._endpoint(self.put, request, pk)
        elif request.method == 'DELETE':
            return self._endpoint(self.delete, request, pk)
        raise HttpError(405, 'Method not allowed')
