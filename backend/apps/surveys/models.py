from datetime import datetime
from typing import Tuple
from django.db import models
from django.db.models import Count, When, Case, F, FloatField, Value
from django.db.models.functions import Greatest, Least, Cast
from django.db.models.functions.math import Power
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from backend.fields import ShortUUIDField
from apps.crowd_bt.constants import (
    GAMMA,
    EPSILON,
    ALPHA_MALICIOUS,
    BETA_MALICIOUS,
    ALPHA,
    BETA,
    TAU,
)


user_model = get_user_model()


class Survey(models.Model):
    uuid: str = ShortUUIDField()
    name: str = models.CharField(max_length=30)
    metadata = JSONField(default=dict)
    active: bool = models.BooleanField(default=True)
    created: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)
    owner: User = models.ForeignKey(
        user_model, on_delete=models.CASCADE, related_name="surveys"
    )

    max_time: int = models.PositiveSmallIntegerField(default=10 * 60)
    min_views: int = models.PositiveSmallIntegerField(default=5)
    allow_concurrent: bool = models.BooleanField(default=True)

    max_annotators: int = models.PositiveIntegerField(default=100)
    max_items: int = models.PositiveIntegerField(default=20)
    max_budget: int = models.PositiveIntegerField(default=500)
    min_budget: int = models.PositiveIntegerField(default=20)

    base_gamma: float = models.FloatField(default=GAMMA)
    epsilon: float = models.FloatField(default=EPSILON)
    tau: float = models.FloatField(default=TAU)

    trust_annotators: bool = models.BooleanField(default=True)
    dynamic_gamma: bool = models.BooleanField(default=True)

    @property
    def budget(self) -> int:
        """Survey's budget

        Returns how many labels can be created by the annotators
        """
        comps = self.get_self_with_computation("sql_budget")
        budget: int = comps.sql_budget
        return budget

    @property
    def consumed_budget(self) -> float:
        """Consumed budget (%)
        What percentage of the budget has already been consumed?
        """
        comps = self.get_self_with_computation("sql_budget")
        consumed_budget: float = comps.sql_consumed_budget
        return consumed_budget

    @property
    def gamma(self) -> float:
        comps = self.get_self_with_computation("sql_gamma")
        gamma: float = comps.sql_gamma
        return gamma

    def get_default_annotator_quality(self) -> Tuple[float, float]:
        if self.trust_annotators:
            return (ALPHA, BETA)
        return (ALPHA_MALICIOUS, BETA_MALICIOUS)

    def get_self_with_computation(self, field: str) -> "Survey":
        if not getattr(self, field, False):
            return Survey.with_sql_computations().get(id=self.id)
        return self

    @classmethod
    def with_sql_computations(cls, queryset=None):
        if queryset is None:
            queryset = cls.objects.all()
        return (
            queryset.annotate(
                sql_budget=Greatest(
                    "min_budget",
                    Least(
                        "max_budget",
                        Count("annotators", distinct=True)
                        * (Count("items", distinct=True) - 1),
                    ),
                )
            )
            .annotate(
                sql_consumed_budget=(
                    Cast(Count("labels", distinct=True), FloatField())
                    / Cast(F("sql_budget"), FloatField())
                )
            )
            .annotate(
                sql_gamma=Case(
                    When(dynamic_gamma=False, then=F("base_gamma")),
                    default=(
                        F("base_gamma")
                        / Power(Value("2"), F("sql_consumed_budget") / F("tau"))
                    ),
                )
            )
        )
