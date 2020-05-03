from typing import Any
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from backend.mixins.prefetch import PrefetchMixin
from backend.mixins.queryfields import QueryFieldsMixin
from apps.surveys.models import Survey
from .models import Item
from .exceptions import ItemsQuotaError


class ItemSerializer(
    PrefetchMixin, QueryFieldsMixin, serializers.HyperlinkedModelSerializer
):

    url = NestedHyperlinkedIdentityField(
        label="This resource's URL",
        view_name="api:item-detail",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )

    survey = serializers.HyperlinkedRelatedField(
        label="Parent survey's URL",
        read_only=True,
        view_name="api:survey-detail",
        lookup_url_kwarg="pk",
    )

    prioritize = NestedHyperlinkedIdentityField(
        label="Prioritize URL",
        read_only=True,
        view_name="api:item-prioritize",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )

    deprioritize = NestedHyperlinkedIdentityField(
        label="Deprioritize URL",
        read_only=True,
        view_name="api:item-deprioritize",
        lookup_url_kwarg="pk",
        parent_lookup_kwargs={"survey_pk": "survey__pk"},
    )

    def create(self, validated_data: Any) -> Item:
        view = self.context["view"]
        survey_id: int = validated_data.get("survey", view.kwargs.get("survey_pk"))
        survey: Survey = Survey.objects.get(id=survey_id)
        if survey.max_items > 0 and survey.max_items <= survey.items.count():
            raise ItemsQuotaError()
        validated_data["survey"] = survey
        item: Item = Item.objects.create(**validated_data)
        return item

    class Meta:
        model = Item
        fields = [
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
