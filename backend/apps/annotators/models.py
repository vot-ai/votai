from typing import Callable, Optional, Any
from numpy.random import random, choice
from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.items.models import Item
from apps.surveys.models import Survey
from backend.custom_types.models import QueryType
from crowd_bt.types import Alpha, Beta, AnnotatorConfidence
from crowd_bt.constants import ALPHA, BETA
from crowd_bt.entropy import expected_information_gain
from crowd_bt.utils import random_argmax
from crowd_bt.online import update_scores, update_annotator


class Annotator(models.Model):
    name: str = models.CharField(max_length=30)
    metadata = JSONField(default=dict)
    active: str = models.BooleanField(default=True)
    survey: Survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="annotators"
    )

    current: Optional[Item] = models.ForeignKey(
        Item, on_delete=models.SET_NULL, related_name="current_annotators", null=True
    )
    previous: Optional[Item] = models.ForeignKey(
        Item, on_delete=models.SET_NULL, related_name="previous_annotators", null=True
    )
    ignored: QueryType[Item] = models.ManyToManyField(Item, related_name="ignored_by")
    viewed: QueryType[Item] = models.ManyToManyField(Item, related_name="viewed_by")

    alpha: Alpha = models.FloatField(default=ALPHA)
    beta: Beta = models.FloatField(default=BETA)

    @property
    def confidence(self) -> AnnotatorConfidence:
        return AnnotatorConfidence(self.alpha, self.beta)

    @property
    def quality(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    def update_confidence(self, winner: Item, loser: Item) -> None:
        new_confidence, _ = update_annotator(winner.score, loser.score, self.confidence)
        self.alpha = new_confidence.alpha
        self.beta = new_confidence.beta
        self.save()

    def bt_update(self, winner: Item, loser: Item) -> None:
        self.update_confidence(winner, loser)
        new_winner_score, new_loser_score = update_scores(
            winner.score, loser.score, self.confidence
        )
        winner.update_score(new_winner_score)
        loser.update_score(new_loser_score)

    def choose_next(self) -> Optional[Item]:
        items: QueryType[Item] = self.survey.items.filter(active=False)

        available: QueryType[Item] = items.exclude(
            id__in=self.ignored.only("id")
        ).exclude(id__in=self.viewed.only("id"))
        prioritized: QueryType[Item] = available.filter(prioritized=True)

        options = prioritized if prioritized.exists() else available

        less_seen: QueryType[Item] = options.annotate(
            viewed_by_count=models.Count("viewed_by")
        ).filter(viewed_by_count__lt=self.survey.min_views)

        options = less_seen if less_seen.exists() else options

        chosen: Optional[Item] = None

        list_options = list(options.only("mu", "sigma_squared"))

        if list_options:
            # epsilon greedy
            if random() < self.survey.epsilon or self.current is None:
                chosen = choice(list_options)
            else:
                previous = self.current.score
                annotator = self.confidence
                func: Callable[[Item], float] = lambda item: expected_information_gain(
                    item.score, previous, annotator, gamma=self.survey.gamma
                )
                chosen = random_argmax(func, list_options)
        return chosen

    def vote(self, current_wins: bool) -> Optional[Item]:
        if self.current is None:
            return None

        # If this is not the first vote
        if self.previous is not None:
            from apps.labels.models import Label

            if current_wins:
                Label.create_label(self, self.current, self.previous)
                self.bt_update(self.current, self.previous)
            else:
                Label.create_label(self, self.previous, self.current)
                self.bt_update(self.previous, self.current)

        return self.update_items()

    def ignore(self) -> Optional[Item]:
        if self.current is None:
            return None

        self.ignored.add(self.current)

        return self.update_items()

    def update_items(self) -> Optional[Item]:
        survey = self.survey
        next_item = self.choose_next()

        if self.current is not None and not survey.allow_concurrent:
            self.current.deactivate()

        self.previous = self.current
        self.current = next_item
        self.save()

        if self.current is not None:
            if not survey.allow_concurrent:
                self.current.activate()
                self.current.schedule_deactivate(survey.max_time)
            self.current.deprioritize()
            self.viewed.add(self.current)
        return self.current

    @classmethod
    def create_annotator(cls, **data: Any) -> "Annotator":
        annotator: Annotator = cls(**data)
        annotator.save()
        annotator.update_items()
        return annotator
