from rest_framework import permissions, viewsets
from backend.permissions import OwnsObject
from backend.mixins import PrefetchQuerysetModelMixin
from rest_condition import Or, And
from .serializers import SurveySerializer
from .models import Survey


class SurveyViewset(PrefetchQuerysetModelMixin, viewsets.ModelViewSet):
    permission_classes = [And(permissions.IsAuthenticated, Or(permissions.IsAdminUser, OwnsObject))]
    ownership_field = "owner"

    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            return qs.filter(owner=self.request.user)
        return qs
