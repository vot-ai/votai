from typing import Any
from rest_framework import serializers
from backend.mixins.prefetch import PrefetchMixin
from backend.mixins.queryfields import QueryFieldsMixin
from .models import Survey


class SurveySerializer(
    PrefetchMixin, QueryFieldsMixin, serializers.HyperlinkedModelSerializer
):

    url = serializers.HyperlinkedIdentityField(
        label="This resource's URL", view_name="api:survey-detail"
    )

    items = serializers.HyperlinkedIdentityField(
        label="URL for a list of items belonging to this survey",
        read_only=True,
        view_name="api:item-list",
        lookup_url_kwarg="survey_pk",
    )

    ranking = serializers.HyperlinkedIdentityField(
        label="URL for the list of ranked items",
        read_only=True,
        view_name="api:item-ranking",
        lookup_url_kwarg="survey_pk",
    )

    annotators = serializers.HyperlinkedIdentityField(
        label="URL for a list of annotators belonging to this survey",
        read_only=True,
        view_name="api:annotator-list",
        lookup_url_kwarg="survey_pk",
    )

    def create(self, validated_data: Any) -> Survey:
        validated_data["owner"] = validated_data.get(
            "owner", self.context["request"].user
        )
        survey: Survey = Survey.objects.create(**validated_data)
        return survey

    class Meta:
        model = Survey
        exclude = ["owner"]
        read_only_fields = ["created", "updated", "owner"]
        select_related_fields = ["owner"]
