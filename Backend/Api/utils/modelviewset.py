import json
from functools import reduce
from typing import Type, Callable

from django.db import models
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.http import require_http_methods

from utils.exception import HttpError, NotFoundError
from utils.modelserializer import ModelSerializer


class ModelViewSet:
    def __init__(self, m: Type[models.Model], s: Type[ModelSerializer]):
        self.decorators: list[Callable] = []
        self.model: Type[models.Model] = m
        self.serializer: Type[ModelSerializer] = s

    def get(self, request, pk):
        instance = self.get_instance(pk)
        serializer = self.serializer(instance=instance)
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(serializer.data))

    def list(self, request):
        qs = self.model.objects.all()
        data = []
        for instance in qs:
            serializer = self.serializer(instance=instance)
            data.append(serializer.data)
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(data))

    def post(self, request):
        data = json.loads(request.body.decode())
        serializer = self.serializer(data=data)
        instance = serializer.save()
        serializer = self.serializer(instance=instance)
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(serializer.data))

    def put(self, request, pk):
        instance = self.get_instance(pk)
        data = json.loads(request.body.decode())
        serializer = self.serializer(instance=instance, data=data)
        serializer.save()
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(serializer.data))

    def delete(self, request, pk):
        instance = self.get_instance(pk)
        serializer = self.serializer(instance=instance)
        instance.delete()
        return HttpResponse(headers={'Content-Type': 'application/json'}, content=json.dumps(serializer.data))

    def get_instance(self, pk):
        qs = self.model.objects.filter(pk=pk)
        if not qs.exists():
            raise NotFoundError()
        return qs.first()

    @staticmethod
    def _endpoint(method: Callable, request, *args, **kwargs):
        try:
            return method(request, *args, **kwargs)
        except HttpError as e:
            return HttpResponse(status=e.status, content=e.content, headers={'Content-Type': e.content_type or 'text/plain'})

    def as_urls(self):
        return [
            path('', reduce(lambda x, y: y(x), self.decorators, require_http_methods(["GET"])(lambda req: self._endpoint(self.list, req))), name='list'),
            path('<int:pk>', reduce(lambda x, y: y(x), self.decorators, require_http_methods(["GET"])(lambda req, pk: self._endpoint(self.get, req, pk))), name='retrieve'),
            path('create/', reduce(lambda x, y: y(x), self.decorators, require_http_methods(["POST"])(lambda req: self._endpoint(self.post, req))), name='create'),
            path('update/<int:pk>/', reduce(lambda x, y: y(x), self.decorators, require_http_methods(["PUT"])(lambda req, pk: self._endpoint(self.put, req, pk))), name='update'),
            path('delete/<int:pk>/', reduce(lambda x, y: y(x), self.decorators, require_http_methods(["DELETE"])(lambda req, pk: self._endpoint(self.delete, req, pk))), name='delete'),
        ]
