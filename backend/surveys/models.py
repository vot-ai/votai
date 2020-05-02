from datetime import datetime
from django.db import models
from crowd_bt.constants import GAMMA, EPSILON


class Survey(models.Model):
    name: str = models.CharField(max_length=30)
    active: bool = models.BooleanField(default=True)
    created: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)

    max_time: int = models.IntegerField(default=10 * 60)
    min_views: int = models.IntegerField(default=5)
    allow_concurrent: bool = models.BooleanField(default=True)

    gamma: float = models.FloatField(default=GAMMA)
    epsilon: float = models.FloatField(default=EPSILON)
