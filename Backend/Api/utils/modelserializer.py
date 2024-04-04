import datetime
import json
from typing import Callable

from django.db import models

from utils.exception import *


class ModelSerializer:
    class Meta:
        model: models.Model = None
        fields: list | str = '__all__'
        excluded_fields: list = []

    def __init__(self, *, instance: models.Model = None, data: dict = None):
        self.none = object()
        self.data = {}
        self.instance = None

        if instance is None and data is None:
            raise ValidationError(json.dumps({"message": "Either instance or data must be provided", "type": "data"}), content_type='application/json')

        if instance is not None and data is not None:
            self._update_instance(instance, data)
        elif instance is not None:
            self.instance = instance
            self._serialize_instance()
        else:
            self._create_instance(data)

    def _update_instance(self, instance, data):
        fields = self._get_fields()
        auto_fields = map(lambda x: x.name, filter(lambda x: x.auto_created, self.Meta.model._meta.fields))
        for field in data:
            if field not in fields:
                raise ValidationError(json.dumps({"message": f"Model {self.Meta.model.__name__} does not have field '{field}'", "type": "data"}),
                                      content_type='application/json')
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
                raise ValidationError(json.dumps({"message": f"Field '{field}' is required", "type": "missing_field", "field": field}),
                                      content_type='application/json')
        for field in self.data:
            if field not in auto_fields:
                deserialize: Callable = getattr(self, f"deserialize_{field}", self._deserialize_field)
                initializer[field] = deserialize(field)
        self._validate_creation_data()
        self.instance = self.Meta.model.objects.create(**initializer)
        self._serialize_instance()

    def _serialize_instance(self):
        self.data = {}
        fields = self._get_fields()
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
            raise ValidationError(json.dumps({"message": f"Field '{field}' is required", "type": "missing_field", "field": field}),
                                  content_type='application/json')
        if isinstance(meta_field, models.ForeignKey):
            return meta_field.related_model.objects.get(pk=value) if isinstance(value, int) else None
        elif isinstance(meta_field, models.DateTimeField):
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S") if isinstance(value, str) else None
        elif isinstance(meta_field, models.DateField):
            return datetime.datetime.strptime(value, "%Y-%m-%d").date() if isinstance(value, str) else None
        return value

    def save(self):
        if not self.instance:
            raise ValidationError(json.dumps({"message": "Cannot save data without instance", "type": "data"}), content_type='application/json')
        self.instance.save()
        return self.instance

    def _validate_data(self):
        fields = self._get_fields()
        for field in self.data:
            if field not in fields:
                raise ValidationError(json.dumps({"message": f"Model {self.Meta.model.__name__} does not have field '{field}'", "type": "data"}),
                                      content_type='application/json')
        # Check model fields for required fields and check if they are present in data
        for field in self.Meta.model._meta.fields:
            if field.name not in self.data and (not field.null and not field.blank):
                raise ValidationError(json.dumps({"message": f"Field '{field.name}' is required", "type": "missing_field", "field": field.name}),
                                      content_type='application/json')

    def _validate_creation_data(self):
        # Check model fields and ensure that they don't break any constraints
        for field in self.Meta.model._meta.fields:
            if field.auto_created:
                continue
            self._validate_field(field)

    def _validate_field(self, field):
        value = self.data.get(field.name, self.none)
        if value is self.none and (not field.null and not field.blank):
            raise ValidationError(json.dumps({"message": f"Field '{field.name}' is required", "type": "missing_field", "field": field.name}),
                                  content_type='application/json')
        if value is not self.none and not field.null and not field.blank:
            if isinstance(field, models.ForeignKey):
                if not field.related_model.objects.filter(pk=value).exists():
                    raise ValidationError(
                        json.dumps({"message": f"Foreign key '{field.name}' does not exist", "type": "invalid_foreign_key", "field": field.name}),
                        content_type='application/json')
            elif isinstance(field, models.DateTimeField):
                try:
                    datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    raise ValidationError(
                        json.dumps({"message": f"Invalid datetime format for field '{field.name}'", "type": "invalid_datetime", "field": field.name}),
                        content_type='application/json')
            elif isinstance(field, models.DateField):
                try:
                    datetime.datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    raise ValidationError(
                        json.dumps({"message": f"Invalid date format for field '{field.name}'", "type": "invalid_date", "field": field.name}),
                        content_type='application/json')
        if value is self.none:
            return

        # Check unique fields
        if field.unique and self.Meta.model.objects.filter(**{field.name: value}).exists():
            raise ValidationError(json.dumps({"message": f"Field '{field.name}' must be unique", "type": "unique_field", "field": field.name}),
                                  content_type='application/json')

        # Check max length
        if self._has(field, "maxlength") and len(value) > field.maxlength:
            raise ValidationError(json.dumps(
                {"message": f"Field '{field.name}' must have at most {field.maxlength} characters", "type": "max_length", "field": field.name}),
                                  content_type='application/json')

        # Check min length
        if self._has(field, "minlength") and len(value) < field.minlength:
            raise ValidationError(json.dumps(
                {"message": f"Field '{field.name}' must have at least {field.minlength} characters", "type": "min_length", "field": field.name}),
                                  content_type='application/json')

        # Check max value
        if self._has(field, "maxvalue") and value > field.maxvalue:
            raise ValidationError(json.dumps(
                {"message": f"Field '{field.name}' must have at most {field.maxvalue}", "type": "max_value", "field": field.name}),
                                  content_type='application/json')

        # Check min value
        if self._has(field, "minvalue") and value < field.minvalue:
            raise ValidationError(json.dumps(
                {"message": f"Field '{field.name}' must have at least {field.minvalue}", "type": "min_value", "field": field.name}),
                                  content_type='application/json')

        # Check choices
        if self._has(field, "choices") and value not in field.choices:
            raise ValidationError(json.dumps(
                {"message": f"Field '{field.name}' must be one of {field.choices}", "type": "choices", "field": field.name}),
                                  content_type='application/json')

    @staticmethod
    def _has(field, attr):
        return hasattr(field, attr) and getattr(field, attr, None) is not None

    def _get_fields(self, exclude=True):
        return filter(
            lambda x: x not in self.Meta.excluded_fields if exclude else True,
            map(
                lambda x: x.name, self.Meta.model._meta.fields
            ) if self.Meta.fields == '__all__' else self.Meta.fields)
