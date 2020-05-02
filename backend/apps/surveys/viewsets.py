from rest_framework import permissions, viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from backend.permissions import OwnsObject
from backend.mixins import PrefetchQuerysetModelMixin
from rest_condition import Or, And
from .serializers import SurveySerializer
from .models import Survey


class SurveyViewset(PrefetchQuerysetModelMixin, viewsets.ModelViewSet):
    """Survey Endpoint

    Allows creating, listing and editing surveys
    """

    swagger_tags = ["Survey"]

    permission_classes = [
        And(permissions.IsAuthenticated, Or(permissions.IsAdminUser, OwnsObject))
    ]
    ownership_field = "owner"

    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            return qs.filter(owner=self.request.user)
        return qs

    @swagger_auto_schema(
        responses={404: "Survey does not exist or you don't have access"},
        manual_parameters=[
            openapi.Parameter(
                SurveySerializer.include_arg_name,
                openapi.IN_QUERY,
                "Selects returned fields, comma separated. Nested fields are supported. Example: `fields=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                SurveySerializer.exclude_arg_name,
                openapi.IN_QUERY,
                "Excludes returned fields, comma separated. Nested fields are supported. Example: `exclude=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def retrieve(self, *args, **kwargs):
        """Survey details
        
        Returns data from a single survey that belongs to the user.
        """
        return super().retrieve(*args, **kwargs)
