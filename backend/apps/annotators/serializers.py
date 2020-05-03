from typing import Any
from rest_framework import serializers
from rest_framework_nested.relations import (
    NestedHyperlinkedIdentityField,
    NestedHyperlinkedRelatedField,
)
from backend.mixins.prefetch import PrefetchMixin
from backend.mixins.queryfields import QueryFieldsMixin
from apps.surveys.models import Survey
from apps.items.serializers import ItemSerializer
from .models import Annotator


class AnnotatorSerializer(
    PrefetchMixin, QueryFieldsMixin, serializers.HyperlinkedModelSerializer
):

    url = NestedHyperlinkedIdentityField(
        label="This resource's URL",
        view_name="api:annotator-detail",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )

    survey = serializers.HyperlinkedRelatedField(
        label="Parent survey's URL",
        read_only=True,
        view_name="api:survey-detail",
        lookup_url_kwarg="pk",
    )

    current = NestedHyperlinkedRelatedField(
        label="Current item's URL",
        read_only=True,
        view_name="api:item-detail",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )
    previous = NestedHyperlinkedRelatedField(
        label="Previous item's URL",
        read_only=True,
        view_name="api:item-detail",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )

    vote = NestedHyperlinkedIdentityField(
        label="Voting URL",
        read_only=True,
        view_name="api:annotator-vote",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )
    skip = NestedHyperlinkedIdentityField(
        label="Skipping URL",
        read_only=True,
        view_name="api:annotator-skip",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )

    def create(self, validated_data: Any) -> Annotator:
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
            "vote",
            "skip",
            "alpha",
            "beta",
            "quality",
        ]
        read_only_fields = [
            "survey",
            "current",
            "previous",
            "alpha",
            "beta",
            "quality",
            "vote",
            "skip",
        ]
        select_related_fields = [
            "survey",
            "current",
            "current__survey",
            "previous",
            "previous__survey",
        ]


class IgnoreSerializer(PrefetchMixin, serializers.ModelSerializer):
    current = ItemSerializer(label="Current item's data", read_only=True)
    previous = ItemSerializer(label="Previous item's data", read_only=True)

    vote = NestedHyperlinkedIdentityField(
        label="Voting URL",
        read_only=True,
        view_name="api:annotator-vote",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )
    skip = NestedHyperlinkedIdentityField(
        label="Skipping URL",
        read_only=True,
        view_name="api:annotator-skip",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )

    def update(self, instance: Annotator, validated_data: Any) -> Annotator:
        instance.ignore()
        return instance

    class Meta:
        model = Annotator
        fields = ["current", "previous", "vote", "skip"]
        read_only_fields = ["current", "previous", "vote", "skip"]
        select_related_fields = [
            "current",
            "current__survey",
            "previous",
            "previous__survey",
        ]


class VoteSerializer(IgnoreSerializer):
    current_wins = serializers.BooleanField(
        label="Whether the current item is the winner. Set to false if the previous is the winner",
        write_only=True,
    )

    def update(self, instance: Annotator, validated_data: Any) -> Annotator:
        instance.vote(**validated_data)
        return instance

    class Meta(IgnoreSerializer.Meta):
        fields = IgnoreSerializer.Meta.fields + ["current_wins"]
