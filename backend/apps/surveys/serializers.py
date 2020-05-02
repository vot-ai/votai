from rest_framework import serializers
from backend.mixins import PrefetchMixin
from .models import Survey


class SurveySerializer(PrefetchMixin, serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="api:survey-detail")

    items = serializers.HyperlinkedIdentityField(
        label="Survey items",
        read_only=True,
        view_name="api:item-list",
        lookup_url_kwarg="survey_pk",
    )

    annotators = serializers.HyperlinkedIdentityField(
        label="Survey annotators",
        read_only=True,
        view_name="api:annotator-list",
        lookup_url_kwarg="survey_pk",
    )

    def create(self, validated_data):
        validated_data["owner"] = validated_data.get(
            "owner", self.context["request"].user
        )
        return Survey.objects.create(**validated_data)

    class Meta:
        model = Survey
        exclude = ["owner"]
        read_only_fields = ["created", "updated", "owner"]
        select_related_fields = ['owner']
