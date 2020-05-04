from rest_framework import serializers
from rest_framework_nested.relations import (
    NestedHyperlinkedIdentityField,
    NestedHyperlinkedRelatedField,
)


class SurveyURL(serializers.HyperlinkedRelatedField):
    def __init__(self, *args, **kwargs):
        initial = {
            "label": "Parent survey's URL",
            "read_only": True,
            "view_name": "api:survey-detail",
            "lookup_field": "uuid",
            "lookup_url_kwarg": "id",
        }
        initial.update(kwargs)
        super().__init__(*args, **initial)


class SurveyHyperlinkedIdentityField(NestedHyperlinkedIdentityField):
    def __init__(self, *args, **kwargs):
        initial = {
            "read_only": True,
            "lookup_field": "uuid",
            "lookup_url_kwarg": "id",
            "parent_lookup_kwargs": {"survey_id": "survey__uuid"},
        }
        initial.update(kwargs)
        super().__init__(*args, **initial)


class SurveyHyperlinkedRelatedField(NestedHyperlinkedRelatedField):
    def __init__(self, *args, **kwargs):
        initial = {
            "read_only": True,
            "lookup_field": "uuid",
            "lookup_url_kwarg": "id",
            "parent_lookup_kwargs": {"survey_id": "survey__uuid"},
        }
        initial.update(kwargs)
        super().__init__(*args, **initial)
