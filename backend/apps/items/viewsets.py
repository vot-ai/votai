from typing import Any
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_condition import And
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from backend.permissions.ownership import OwnsObject
from backend.mixins.prefetch import PrefetchQuerysetModelMixin
from backend.mixins.queryfields import QueryFieldsMixin
from backend.custom_types.models import QueryType
from .serializers import ItemSerializer, PrioritizeSerializer, DeprioritizeSerializer
from .models import Item


class SurveyItemViewset(
    PrefetchQuerysetModelMixin, QueryFieldsMixin, viewsets.ModelViewSet
):

    swagger_tags = ["Items"]

    lookup_field = "uuid"
    lookup_url_kwarg = "id"

    permission_classes = [And(permissions.IsAuthenticated, OwnsObject)]
    ownership_field = "survey.owner"

    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_queryset(self) -> QueryType[Item]:
        survey_id = self.kwargs.get("survey_id")
        qs: QueryType[Item] = super().get_queryset().filter(survey__uuid=survey_id)
        if self.action == "ranking":
            qs = qs.order_by("-mu")
        return qs

    def get_serializer_class(self) -> Any:
        if self.action == "prioritize":
            return PrioritizeSerializer
        if self.action == "deprioritize":
            return DeprioritizeSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["get"])
    def ranking(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Ranked items

        Returns the list of items ranked from best to worst.
        """
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def prioritize(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Prioritize item

        Prioritizes an item so it is assigned to an annotator faster.
        """
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def deprioritize(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Deprioritize item

        Deprioritizes item. Note that this happens automatically once it is assigned to an annotator.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(responses={400: "Request data is missing or contains errors"})
    def create(self, *args: Any, **kwargs: Any) -> Response:
        """Create a new item

        Creates a new item under the provided survey
        """
        return super().create(*args, **kwargs)

    @swagger_auto_schema(
        responses={404: "Item does not exist or you don't have access"},
        manual_parameters=[
            openapi.Parameter(
                ItemSerializer.include_arg_name,
                openapi.IN_QUERY,
                "Selects returned fields, comma separated. Nested fields are supported. Example: `fields=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                ItemSerializer.exclude_arg_name,
                openapi.IN_QUERY,
                "Excludes returned fields, comma separated. Nested fields are supported. Example: `exclude=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def retrieve(self, *args: Any, **kwargs: Any) -> Response:
        """Get details from an item

        Returns data from a single item that belongs to the survey.
        """
        return super().retrieve(*args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                ItemSerializer.include_arg_name,
                openapi.IN_QUERY,
                "Selects returned fields, comma separated. Nested fields are supported. Example: `fields=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                ItemSerializer.exclude_arg_name,
                openapi.IN_QUERY,
                "Excludes returned fields, comma separated. Nested fields are supported. Example: `exclude=field1,field2{sub_field1, sub_field2}`",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def list(self, *args: Any, **kwargs: Any) -> Response:
        """List surveys's items

        Lists all of the survey's items
        """
        return super().list(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            404: "Item does not exist or you don't have access",
            400: "Request data is missing or contains errors",
        }
    )
    def update(self, *args: Any, **kwargs: Any) -> Response:
        """Update an item

        Updates all fields of the item
        """
        return super().update(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            404: "Item does not exist or you don't have access",
            400: "Request data contains errors",
        }
    )
    def partial_update(self, *args: Any, **kwargs: Any) -> Response:
        """Partially update an item

        Updates some fields of the item
        """
        return super().partial_update(*args, **kwargs)

    @swagger_auto_schema(
        responses={404: "Item does not exist or you don't have access"}
    )
    def destroy(self, *args: Any, **kwargs: Any) -> Response:
        """Remove item

        Deletes an item and all of its related contents
        """
        return super().destroy(*args, **kwargs)
