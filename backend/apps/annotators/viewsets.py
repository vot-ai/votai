from rest_framework import permissions, viewsets, exceptions
from rest_condition import And
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from backend.permissions import OwnsObject
from backend.mixins import PrefetchQuerysetModelMixin, QueryFieldsMixin
from apps.surveys.exceptions import InactiveSurveyError
from apps.surveys.models import Survey
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

    def get_queryset(self):
        survey_pk = self.kwargs.get("survey_pk")
        qs = super().get_queryset().filter(survey=survey_pk)
        return qs

    def get_serializer_class(self):
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
    def vote(self, request, **kwargs):
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
    def skip(self, request, **kwargs):
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
    def create(self, *args, **kwargs):
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
    def retrieve(self, *args, **kwargs):
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
    def list(self, *args, **kwargs):
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
    def update(self, *args, **kwargs):
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
    def partial_update(self, *args, **kwargs):
        """Partially update an annotator
        
        Updates some fields of the annotator
        """
        return super().partial_update(*args, **kwargs)

    @swagger_auto_schema(
        responses={404: "Annotator does not exist or you don't have access"}
    )
    def destroy(self, *args, **kwargs):
        """Remove annotator
        
        Deletes an annotator and all of its related contents
        """
        return super().destroy(*args, **kwargs)
