import datetime
from typing import Callable

from django.db import models

from utils.exception import *


class ModelSerializer:
    class Meta:
        model: models.Model = None
        fields: list | str = '__all__'

    def __init__(self, *, instance: models.Model = None, data: dict = None):
        self.none = object()
        self.data = {}
        self.instance = None

        if not instance and not data:
            raise ValueError("Either instance or data must be provided")

        if instance is not None and data is not None:
            self._update_instance(instance, data)
        elif instance:
            self.instance = instance
            self._serialize_instance()
        else:
            self._create_instance(data)

    def _update_instance(self, instance, data):
        fields = map(lambda x: x.name, self.Meta.model._meta.fields) if self.Meta.fields == '__all__' else self.Meta.fields
        auto_fields = map(lambda x: x.name, filter(lambda x: x.auto_created, self.Meta.model._meta.fields))
        for field in data:
            if field not in fields:
                raise ValidationError(f"Model {self.Meta.model.__name__} does not have field '{field}'")
        self.data = data
        for field in data:
            if field not in auto_fields:
                deserialize: Callable = getattr(self, f"deserialize_{field}", self._deserialize_field)
                setattr(instance, field, deserialize(field))
        self.instance = instance
        self._serialize_instance()

    def _create_instance(self, data):
        self.data = data
        initializer = {}
        required_fields = map(lambda x: x.name, filter(lambda x: not x.null and not x.blank and not x.auto_created, self.Meta.model._meta.fields))
        auto_fields = map(lambda x: x.name, filter(lambda x: x.auto_created, self.Meta.model._meta.fields))
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Field '{field}' is required")
        for field in self.data:
            if field not in auto_fields:
                deserialize: Callable = getattr(self, f"deserialize_{field}", self._deserialize_field)
                initializer[field] = deserialize(field)
        self.instance = self.Meta.model.objects.create(**initializer)
        self._serialize_instance()

    def _serialize_instance(self):
        self.data = {}
        fields = map(lambda x: x.name, self.Meta.model._meta.fields) if self.Meta.fields == '__all__' else self.Meta.fields
        for field in fields:
            serialize: Callable = getattr(self, f"serialize_{field}", self._serialize_value)
            self.data[field] = serialize(getattr(self.instance, field))

    @staticmethod
    def _serialize_value(value):
        if isinstance(value, models.Model):
            return value.pk
        elif isinstance(value, datetime.datetime):
            return f"{value:%Y-%m-%d %H:%M:%S}"
        elif isinstance(value, datetime.date):
            return f"{value:%Y-%m-%d}"
        elif not isinstance(value, (str, int, float, bool, dict, list)):
            return str(value)
        return value

    def _deserialize_field(self, field):
        meta_field = self.Meta.model._meta.get_field(field)
        value = self.data.get(field, self.none)
        if value is self.none:
            raise ValidationError(f"Field '{field}' is required")
        if isinstance(meta_field, models.ForeignKey):
            return meta_field.related_model.objects.get(pk=value) if isinstance(value, int) else None
        elif isinstance(meta_field, models.DateTimeField):
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S") if isinstance(value, str) else None
        elif isinstance(meta_field, models.DateField):
            return datetime.datetime.strptime(value, "%Y-%m-%d").date() if isinstance(value, str) else None
        return value

    def save(self):
        if not self.instance:
            raise ValidationError("Cannot save data without instance")
        self.instance.save()
        return self.instance

    def _validate_data(self):
        fields = map(lambda x: x.name, self.Meta.model._meta.fields) if self.Meta.fields == '__all__' else self.Meta.fields
        for field in self.data:
            if field not in fields:
                raise ValidationError(f"Model {self.Meta.model.__name__} does not have field '{field}'")
        # Check model fields for required fields and check if they are present in data
        for field in self.Meta.model._meta.fields:
            if field.name not in self.data and (not field.null and not field.blank):
                raise ValidationError(f"Field '{field.name}' is required")
