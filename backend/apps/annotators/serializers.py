from typing import Any
from rest_framework import serializers
from backend.mixins.prefetch import PrefetchMixin
from backend.mixins.queryfields import QueryFieldsMixin
from backend.fields import SelfUUIDField, NestedURLField
from apps.surveys.models import Survey
from apps.surveys.fields import (
    SurveyURL,
    SurveyHyperlinkedIdentityField,
    SurveyHyperlinkedRelatedField,
)
from apps.items.serializers import ItemSerializer
from .models import Annotator
from .exceptions import AnnotatorsQuotaError


class AnnotatorSerializer(
    PrefetchMixin, QueryFieldsMixin, serializers.HyperlinkedModelSerializer
):

    id = SelfUUIDField()
    url = NestedURLField(view_name="api:annotator-detail")

    survey = SurveyURL()

    current = SurveyHyperlinkedRelatedField(
        label="Current item's URL", view_name="api:item-detail",
    )
    previous = SurveyHyperlinkedRelatedField(
        label="Previous item's URL", view_name="api:item-detail",
    )

    vote = SurveyHyperlinkedIdentityField(
        label="Voting URL", view_name="api:annotator-vote",
    )
    skip = SurveyHyperlinkedIdentityField(
        label="Skipping URL", view_name="api:annotator-skip",
    )

    def create(self, validated_data: Any) -> Annotator:
        view = self.context["view"]
        survey_id: int = validated_data.get("survey", view.kwargs.get("survey_id"))
        survey: Survey = Survey.objects.get(uuid=survey_id)
        if (
            survey.max_annotators > 0
            and survey.max_annotators <= survey.annotators.count()
        ):
            raise AnnotatorsQuotaError()
        validated_data["survey"] = survey
        return Annotator.create_annotator(**validated_data)

    class Meta:
        model = Annotator
        fields = [
            "id",
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
            "id",
            "survey",
            "current",
            "previous",
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

    vote = SurveyHyperlinkedIdentityField(
        label="Voting URL", view_name="api:annotator-vote",
    )
    skip = SurveyHyperlinkedIdentityField(
        label="Skipping URL", view_name="api:annotator-skip",
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
