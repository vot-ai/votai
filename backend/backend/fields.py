from typing import Any
from django.db.models import CharField
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
import shortuuid


def default_gen() -> Any:
    return shortuuid.uuid()[:12]


# Model fields


class ShortUUIDField(CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.update(
            {
                "max_length": 22,
                "editable": False,
                "blank": True,
                "null": False,
                "unique": True,
                "default": default_gen,
                "auto_created": True,
            }
        )
        super().__init__(*args, **kwargs)


# Serializer fields


class SelfUUIDField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        initial = {"read_only": True, "source": "uuid", "label": "This resource's ID"}
        initial.update(kwargs)
        super().__init__(*args, **initial)


class NestedURLField(NestedHyperlinkedIdentityField):
    def __init__(self, *args, **kwargs):
        initial = {
            "label": "This resource's URL",
            "lookup_field": "uuid",
            "lookup_url_kwarg": "id",
            "parent_lookup_kwargs": {"survey_id": "survey__uuid"},
        }
        initial.update(kwargs)
        super().__init__(*args, **initial)
