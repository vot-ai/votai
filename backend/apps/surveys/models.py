from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from crowd_bt.constants import GAMMA, EPSILON


user_model = get_user_model()


class Survey(models.Model):
    name: str = models.CharField(max_length=30)
    metadata = JSONField()
    active: bool = models.BooleanField(default=True)
    created: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)
    owner: user_model = models.ForeignKey(
        user_model, on_delete=models.CASCADE, related_name="surveys"
    )

    max_time: int = models.IntegerField(default=10 * 60)
    min_views: int = models.IntegerField(default=5)
    allow_concurrent: bool = models.BooleanField(default=True)

    gamma: float = models.FloatField(default=GAMMA)
    epsilon: float = models.FloatField(default=EPSILON)