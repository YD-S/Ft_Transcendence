from typing import Type

from django.db import models
from django.http import JsonResponse

from common.request import HttpRequest, ViewMixin
from utils.exception import NotFoundError
from utils.modelserializer import ModelSerializer


class ModelViewSet(ViewMixin):
    model: Type[models.Model]
    serializer: Type[ModelSerializer]

    def __init__(self, request: HttpRequest, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def get(self, request: HttpRequest, pk, *args, **kwargs):
        instance = self.get_instance(pk)
        serializer = self.serializer(instance=instance)
        return JsonResponse(serializer.data)

    def list(self, request: HttpRequest, *args, **kwargs):
        qs = self.model.objects.all()
        data = []
        for instance in qs:
            serializer = self.serializer(instance=instance)
            data.append(serializer.data)
        return JsonResponse(data, safe=False)

    def post(self, request: HttpRequest, *args, **kwargs):
        serializer = self.serializer(data=request.json())
        instance = serializer.save()
        serializer = self.serializer(instance=instance)
        return JsonResponse(serializer.data)

    def put(self, request: HttpRequest, pk: int, *args, **kwargs):
        instance = self.get_instance(pk)
        data = request.json()
        serializer = self.serializer(instance=instance, data=data)
        serializer.save()
        return JsonResponse(serializer.data)

    def delete(self, request: HttpRequest, pk: int, *args, **kwargs):
        instance = self.get_instance(pk)
        serializer = self.serializer(instance=instance)
        instance.delete()
        return JsonResponse(serializer.data)

    @classmethod
    def get_instance(cls, pk: int):
        qs = cls.model.objects.filter(pk=pk)
        if not qs.exists():
            raise NotFoundError()
        return qs.first()

    @classmethod
    def as_view(cls, detail=False):
        def view(request: HttpRequest, *args, **kwargs):
            self = cls(request, *args, **kwargs)
            return self.dispatch(request, *args, **{**kwargs, '__detail': detail})

        return view
