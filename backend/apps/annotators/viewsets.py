from rest_framework import permissions, viewsets
from rest_condition import And
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.permissions import OwnsObject
from backend.mixins import PrefetchQuerysetModelMixin, QueryFieldsMixin
from .serializers import AnnotatorSerializer, VoteSerializer, IgnoreSerializer
from .models import Annotator


class SurveyAnnotatorViewset(
    PrefetchQuerysetModelMixin, QueryFieldsMixin, viewsets.ModelViewSet
):
    permission_classes = [And(permissions.IsAuthenticated, OwnsObject)]
    ownership_field = "survey.owner"

    serializer_class = AnnotatorSerializer
    queryset = Annotator.objects.all()

    def get_queryset(self):
        survey_pk = self.kwargs.get("survey_pk")
        qs = super().get_queryset().filter(survey=survey_pk)
        return qs

    @action(detail=True, methods=["post"])
    def vote(self, request, **kwargs):
        annotator = self.get_object()
        serializer = VoteSerializer(
            annotator, data=request.data, context={"request": request}
        )
        serializer.is_valid(True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def ignore(self, request, **kwargs):
        annotator = self.get_object()
        serializer = IgnoreSerializer(
            annotator, data=request.data, context={"request": request}
        )
        serializer.is_valid(True)
        serializer.save()
        return Response(serializer.data)
