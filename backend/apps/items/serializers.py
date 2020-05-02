from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from backend.mixins import PrefetchMixin, QueryFieldsMixin
from apps.surveys.models import Survey
from .models import Item


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

    def create(self, validated_data):
        view = self.context["view"]
        survey_id = validated_data.get("survey", view.kwargs.get("survey_pk"))
        if survey_id:
            validated_data["survey"] = Survey.objects.get(id=survey_id)
        return Item.objects.create(**validated_data)

    class Meta:
        model = Item
        fields = [
            "url",
            "survey",
            "name",
            "metadata",
            "active",
            "prioritized",
            "mu",
            "sigma_squared",
        ]
        read_only_fields = ["mu", "sigma_squared", "survey", "active", "prioritized"]
        select_related_fields = ["survey"]


class PrioritizeSerializer(ItemSerializer):
    def create(self, validated_data):
        raise NotImplementedError("Creation is not allowed")

    def update(self, instance: Item, validated_data):
        instance.prioritize()
        return instance

    class Meta(ItemSerializer.Meta):
        read_only_fields = ItemSerializer.Meta.fields


class DeprioritizeSerializer(PrioritizeSerializer):
    def update(self, instance: Item, validated_data):
        instance.deprioritize()
        return instance
