from typing import Any, Dict
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_condition import And
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from backend.permissions.ownership import OwnsObject
from backend.mixins.prefetch import PrefetchQuerysetModelMixin
from backend.mixins.queryfields import QueryFieldsMixin
from backend.custom_types.models import QueryType
from apps.surveys.exceptions import InactiveSurveyError
from .exceptions import InactiveAnnotatorError
from .serializers import AnnotatorSerializer, VoteSerializer, IgnoreSerializer
from .models import Annotator


class SurveyAnnotatorViewset(
    PrefetchQuerysetModelMixin, QueryFieldsMixin, viewsets.ModelViewSet
):
    swagger_tags = ["Annotator"]

    permission_classes = [And(permissions.IsAuthenticated, OwnsObject)]
    ownership_field = "survey.owner"

    serializer_class = AnnotatorSerializer
    queryset = Annotator.objects.all()

    def get_queryset(self) -> QueryType[Annotator]:
        survey_pk = self.kwargs.get("survey_pk")
        qs: QueryType[Annotator] = super().get_queryset().filter(survey=survey_pk)
        return qs

    def get_serializer_class(self) -> Any:
        if self.action == "vote":
            return VoteSerializer
        if self.action == "skip":
            return IgnoreSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(
        responses={
            400: "Request data is missing or contains errors, or Annotator/Survey are inactive"
        }
    )
    @action(detail=True, methods=["post"])
    def vote(self, request: Request, **kwargs: Any) -> Response:
        """Vote for an item

        Votes for an item as the annotator. The parameter provided `current_wins` represents whether the current item is better than the previous. **This cannot be undone.**
        """
        annotator = self.get_object()
        if not annotator.active:
            raise InactiveAnnotatorError(
                "Cannot vote because the annotator is inactive"
            )

        if not annotator.survey.active:
            raise InactiveSurveyError("Cannot vote because the survey is inactive")
        return super().update(request, **kwargs)

    @swagger_auto_schema(responses={400: "Annotator/Survey are inactive"})
    @action(detail=True, methods=["post"])
    def skip(self, request: Request, **kwargs: Any) -> Response:
        """Skip the annotator's current item

        Skips the current item being evaluated by the annotator. **This cannot be undone.**
        """
        annotator = self.get_object()
        if not annotator.active:
            raise InactiveAnnotatorError(
                "Cannot skip because the annotator is inactive"
            )

        if not annotator.survey.active:
            raise InactiveSurveyError("Cannot skip because the survey is inactive")
        return super().update(request, **kwargs)

    @swagger_auto_schema(responses={400: "Request data is missing or contains errors"})
    def create(self, *args: Any, **kwargs: Any) -> Response:
        """Create a new annotator

        Creates a new annotator under the provided survey
        """
        return super().create(*args, **kwargs)

    @swagger_auto_schema(
        responses={404: "Annotator does not exist or you don't have access"},
        manual_parameters=[
            openapi.Parameter(
                AnnotatorSerializer.include_arg_name,
                openapi.IN_QUERY,
                "Selects returned fields, comma separated. Nested fields are supported. Example: `fields=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                AnnotatorSerializer.exclude_arg_name,
                openapi.IN_QUERY,
                "Excludes returned fields, comma separated. Nested fields are supported. Example: `exclude=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def retrieve(self, *args: Any, **kwargs: Any) -> Response:
        """Get details from an annotator

        Returns data from a single annotator that belongs to the survey.
        """
        return super().retrieve(*args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                AnnotatorSerializer.include_arg_name,
                openapi.IN_QUERY,
                "Selects returned fields, comma separated. Nested fields are supported. Example: `fields=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                AnnotatorSerializer.exclude_arg_name,
                openapi.IN_QUERY,
                "Excludes returned fields, comma separated. Nested fields are supported. Example: `exclude=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def list(self, *args: Any, **kwargs: Any) -> Response:
        """List surveys's annotators

        Lists all of the survey's annotators
        """
        return super().list(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            404: "Annotator does not exist or you don't have access",
            400: "Request data is missing or contains errors",
        }
    )
    def update(self, *args: Any, **kwargs: Any) -> Response:
        """Update an annotator

        Updates all fields of the annotator
        """
        return super().update(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            404: "Annotator does not exist or you don't have access",
            400: "Request data contains errors",
        }
    )
    def partial_update(self, *args: Any, **kwargs: Any) -> Response:
        """Partially update an annotator

        Updates some fields of the annotator
        """
        return super().partial_update(*args, **kwargs)

    @swagger_auto_schema(
        responses={404: "Annotator does not exist or you don't have access"}
    )
    def destroy(self, *args: Any, **kwargs: Any) -> Response:
        """Remove annotator

        Deletes an annotator and all of its related contents
        """
        return super().destroy(*args, **kwargs)
