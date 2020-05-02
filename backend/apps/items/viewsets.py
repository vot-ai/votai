from rest_framework import permissions, viewsets
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
        survey_pk = self.kwargs.get('survey_pk')
        qs = super().get_queryset().filter(survey=survey_pk)
        return qs
