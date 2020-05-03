from datetime import datetime
from typing import Optional
from django.db import models
from apps.surveys.models import Survey
from apps.annotators.models import Annotator
from apps.items.models import Item


class Label(models.Model):
    datetime: datetime = models.DateTimeField(auto_now_add=True)
    survey: Survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="labels"
    )
    annotator: Optional[Annotator] = models.ForeignKey(
        Annotator, on_delete=models.SET_NULL, related_name="labels", null=True
    )
    winner: Item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="winner_labels"
    )
    loser: Item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="loser_labels"
    )

    @classmethod
    def create_label(cls, annotator: Annotator, winner: Item, loser: Item) -> "Label":
        label = cls(
            survey=annotator.survey, annotator=annotator, winner=winner, loser=loser
        )
        label.save()
        return label
