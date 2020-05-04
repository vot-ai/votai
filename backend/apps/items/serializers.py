from typing import Any
from rest_framework import serializers
from backend.mixins.prefetch import PrefetchMixin
from backend.mixins.queryfields import QueryFieldsMixin
from backend.fields import SelfUUIDField, NestedURLField
from apps.surveys.models import Survey
from apps.surveys.fields import (
    SurveyURL,
    SurveyHyperlinkedIdentityField,
)
from .models import Item
from .exceptions import ItemsQuotaError


class ItemSerializer(
    PrefetchMixin, QueryFieldsMixin, serializers.HyperlinkedModelSerializer
):

    id = SelfUUIDField()
    url = NestedURLField(view_name="api:item-detail")

    survey = SurveyURL()

    prioritize = SurveyHyperlinkedIdentityField(
        label="Prioritize URL", view_name="api:item-prioritize",
    )

    deprioritize = SurveyHyperlinkedIdentityField(
        label="Deprioritize URL", view_name="api:item-deprioritize",
    )

    def create(self, validated_data: Any) -> Item:
        view = self.context["view"]
        survey_id: int = validated_data.get("survey", view.kwargs.get("survey_id"))
        survey: Survey = Survey.objects.get(uuid=survey_id)
        if survey.max_items > 0 and survey.max_items <= survey.items.count():
            raise ItemsQuotaError()
        validated_data["survey"] = survey
        item: Item = Item.objects.create(**validated_data)
        return item

    class Meta:
        model = Item
        fields = [
            "id",
            "url",
            "survey",
            "prioritize",
            "deprioritize",
            "name",
            "metadata",
            "active",
            "prioritized",
            "mu",
            "sigma_squared",
        ]
        read_only_fields = [
            "id",
            "mu",
            "sigma_squared",
            "survey",
            "prioritize",
            "deprioritize",
            "active",
            "prioritized",
        ]
        select_related_fields = ["survey"]


class PrioritizeSerializer(ItemSerializer):
    def update(self, instance: Item, validated_data: Any) -> Item:
        instance.prioritize()
        return instance

    class Meta(ItemSerializer.Meta):
        read_only_fields = ItemSerializer.Meta.fields


class DeprioritizeSerializer(PrioritizeSerializer):
    def update(self, instance: Item, validated_data: Any) -> Item:
        instance.deprioritize()
        return instance
