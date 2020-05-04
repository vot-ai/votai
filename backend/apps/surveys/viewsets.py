from typing import Any
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_condition import Or, And
from backend.permissions.ownership import OwnsObject
from backend.mixins.prefetch import PrefetchQuerysetModelMixin
from backend.custom_types.models import QueryType
from .serializers import SurveySerializer
from .models import Survey


class SurveyViewset(PrefetchQuerysetModelMixin, viewsets.ModelViewSet):
    """Survey Endpoint

    Allows creating, listing and editing surveys
    """

    swagger_tags = ["Survey"]

    lookup_field = "uuid"
    lookup_url_kwarg = "id"

    permission_classes = [
        And(permissions.IsAuthenticated, Or(permissions.IsAdminUser, OwnsObject))
    ]
    ownership_field = "owner"

    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get_queryset(self) -> QueryType[Survey]:
        qs: QueryType[Survey] = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(owner=self.request.user)
        return qs

    @swagger_auto_schema(responses={400: "Request data is missing or contains errors"})
    def create(self, *args: Any, **kwargs: Any) -> Response:
        """Create a new survey

        Creates a new survey under your user and returns its data
        """
        return super().create(*args, **kwargs)

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
    def retrieve(self, *args: Any, **kwargs: Any) -> Response:
        """Get details from a survey

        Returns data from a single survey that belongs to the user.
        """
        return super().retrieve(*args, **kwargs)

    @swagger_auto_schema(
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
    def list(self, *args: Any, **kwargs: Any) -> Response:
        """List user's surveys

        Lists all of the user's surveys
        """
        return super().list(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            404: "Survey does not exist or you don't have access",
            400: "Request data is missing or contains errors",
        }
    )
    def update(self, *args: Any, **kwargs: Any) -> Response:
        """Update a survey

        Updates all fields of the survey
        """
        return super().update(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            404: "Survey does not exist or you don't have access",
            400: "Request data contains errors",
        }
    )
    def partial_update(self, *args: Any, **kwargs: Any) -> Response:
        """Partially update a survey

        Updates some fields of the survey
        """
        return super().partial_update(*args, **kwargs)

    @swagger_auto_schema(
        responses={404: "Survey does not exist or you don't have access"}
    )
    def destroy(self, *args: Any, **kwargs: Any) -> Response:
        """Remove survey

        Deletes a survey and all of its related contents
        """
        return super().destroy(*args, **kwargs)
