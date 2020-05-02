from typing import Callable, Optional
from numpy.random import random, choice
from django.db import models
from django.contrib.postgres.fields import JSONField
from items.models import Item
from surveys.models import Survey
from custom_types import QueryType
from crowd_bt.types import Alpha, Beta, AnnotatorConfidence
from crowd_bt.constants import ALPHA, BETA
from crowd_bt.entropy import expected_information_gain
from crowd_bt.utils import random_argmax
from crowd_bt.online import update_scores, update_annotator


class Annotator(models.Model):
    name: str = models.CharField(max_length=30)
    metadata = JSONField(name="Metadata")
    active: str = models.BooleanField(default=True)
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="annotators"
    )

    current: Item = models.ForeignKey(
        Item, on_delete=models.SET_NULL, related_name="current_annotators", null=True
    )
    previous: Item = models.ForeignKey(
        Item, on_delete=models.SET_NULL, related_name="previous_annotators", null=True
    )
    ignored: QueryType[Item] = models.ManyToManyField(Item, related_name="ignored_by")
    viewed: QueryType[Item] = models.ManyToManyField(Item, related_name="viewed_by")

    alpha: Alpha = models.FloatField(default=ALPHA)
    beta: Beta = models.FloatField(default=BETA)

    @property
    def confidence(self):
        return AnnotatorConfidence(self.alpha, self.beta)

    @property
    def quality(self):
        return self.alpha / (self.alpha + self.beta)

    def update_confidence(self, winner: Item, loser: Item):
        new_confidence, _ = update_annotator(winner.score, loser.score, self.confidence)
        self.alpha = new_confidence.alpha
        self.beta = new_confidence.beta
        self.save()

    def bt_update(self, winner: Item, loser: Item):
        self.update_confidence(winner, loser)
        new_winner_score, new_loser_score = update_scores(
            winner.score, loser.score, self.confidence
        )
        winner.update_score(new_winner_score)
        loser.update_score(new_loser_score)

    def choose_next(self):
        # Get all items and filter inactive if survey does not allow concurrent
        items: QueryType[Item] = self.survey.items.all()
        if not self.survey.allow_concurrent:
            items = items.filter(active=False)

        available: QueryType[Item] = items.exclude(
            id__in=self.ignored.only("id")
        ).exclude(id__in=self.viewed.only("id"))
        prioritized: QueryType[Item] = available.filter(prioritized=True)

        options = prioritized if prioritized.exists() else available

        less_seen: QueryType[Item] = options.annotate(
            viewed_by_count=models.Count("viewed_by")
        ).filter(viewed_by_count__lt=self.survey.min_views)

        options = less_seen if less_seen.exists() else options

        if options:
            options = list(options)
            # epsilon greedy
            if random() < self.survey.epsilon or self.current is None:
                choosen: Optional[Item] = choice(options)
            else:
                previous = self.current.score
                annotator = self.confidence
                func: Callable[[Item], float] = lambda item: expected_information_gain(
                    item.score, previous, annotator, gamma=self.survey.gamma
                )
                choosen: Optional[Item] = random_argmax(func, list(options))
        else:
            choosen: Optional[Item] = None
        return choosen

    def vote(self, current_wins: bool):
        if self.current is None:
            return None

        # If this is not the first vote
        if self.previous is not None:
            from labels.models import Label

            if current_wins:
                Label.create_label(self, self.current, self.previous)
                self.bt_update(self.current, self.previous)
            else:
                Label.create_label(self, self.previous, self.current)
                self.bt_update(self.previous, self.current)

        # Get next item
        next_item = self.choose_next()

        if self.survey.allow_concurrent:
            self.current.deactivate()

        # Swap previous and current
        self.previous = self.current
        self.current = next_item
        self.save()

        if next_item is not None:
            if self.survey.allow_concurrent:
                self.current.activate()
            self.current.deprioritize()
            self.viewed.add(self.current)

        return self.current

    def ignore(self):
        if self.current is None:
            return None

        next_item = self.choose_next()

        if self.survey.allow_concurrent:
            self.current.deactivate()

        self.ignored.add(self.current)
        self.current = next_item
        self.save()

        if self.current is not None:
            if self.survey.allow_concurrent:
                self.current.activate()
            self.current.deprioritize()

        return self.current
