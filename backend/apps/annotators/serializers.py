from rest_framework import serializers
from rest_framework_nested.relations import (
    NestedHyperlinkedIdentityField,
    NestedHyperlinkedRelatedField,
)
from backend.mixins import PrefetchMixin
from apps.surveys.models import Survey
from apps.items.serializers import ItemSerializer
from .models import Annotator


class IgnoreSerializer(PrefetchMixin, serializers.ModelSerializer):
    current = ItemSerializer(read_only=True)
    previous = ItemSerializer(read_only=True)

    def create(self, validated_data):
        raise NotImplementedError("Creation is not allowed")

    def update(self, instance: Annotator, validated_data):
        instance.ignore()
        return instance

    class Meta:
        model = Annotator
        fields = ["current", "previous"]
        select_related_fields = [
            "current",
            "current__survey",
            "previous",
            "previous__survey",
        ]


class VoteSerializer(IgnoreSerializer):
    current_wins = serializers.BooleanField(write_only=True)

    def update(self, instance: Annotator, validated_data):
        instance.vote(**validated_data)
        return instance

    class Meta(IgnoreSerializer.Meta):
        fields = IgnoreSerializer.Meta.fields + ["current_wins"]


class AnnotatorSerializer(PrefetchMixin, serializers.HyperlinkedModelSerializer):

    url = NestedHyperlinkedIdentityField(
        view_name="api:annotator-detail",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )

    survey = serializers.HyperlinkedRelatedField(
        label="Survey",
        read_only=True,
        view_name="api:survey-detail",
        lookup_url_kwarg="pk",
    )

    current = NestedHyperlinkedRelatedField(
        label="Current item",
        read_only=True,
        view_name="api:item-detail",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )
    previous = NestedHyperlinkedRelatedField(
        label="Previous item",
        read_only=True,
        view_name="api:item-detail",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )

    def create(self, validated_data):
        view = self.context["view"]
        survey_id = validated_data.get("survey", view.kwargs.get("survey_pk"))
        if survey_id:
            validated_data["survey"] = Survey.objects.get(id=survey_id)
        return Annotator.create_annotator(**validated_data)

    class Meta:
        model = Annotator
        fields = [
            "url",
            "survey",
            "name",
            "metadata",
            "active",
            "current",
            "previous",
            "alpha",
            "beta",
            "quality",
        ]
        read_only_fields = [
            "active",
            "survey",
            "current",
            "previous",
            "ignored",
            "viewed",
            "alpha",
            "beta",
            "quality",
        ]
        select_related_fields = [
            "survey",
            "current",
            "current__survey",
            "previous",
            "previous__survey",
        ]
