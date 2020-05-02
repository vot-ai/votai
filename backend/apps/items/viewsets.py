from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_condition import And
from backend.permissions import OwnsObject
from backend.mixins import PrefetchQuerysetModelMixin
from .serializers import ItemSerializer
from .models import Item


class SurveyItemViewset(PrefetchQuerysetModelMixin, viewsets.ModelViewSet):
    permission_classes = [And(permissions.IsAuthenticated, OwnsObject)]
    ownership_field = "survey.owner"

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_queryset(self):
        survey_pk = self.kwargs.get("survey_pk")
        qs = super().get_queryset().filter(survey=survey_pk)
        if self.action == "ranking":
            qs = qs.order_by("-mu")
        return qs

    @action(detail=False, methods=["get"])
    def ranking(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def prioritize(self, request, *args, **kwargs):
        instance: Item = self.get_object()
        instance.prioritize()
        return self.retrieve(request, *args, **kwargs)
    
    @action(detail=True, methods=["post"])
    def deprioritize(self, request, *args, **kwargs):
        instance: Item = self.get_object()
        instance.deprioritize()
        return self.retrieve(request, *args, **kwargs)
