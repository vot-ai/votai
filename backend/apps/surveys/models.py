from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from backend.fields import ShortUUIDField
from apps.crowd_bt.constants import GAMMA, EPSILON


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

    max_annotators: int = models.PositiveIntegerField(default=50)
    max_items: int = models.PositiveIntegerField(default=100)

    gamma: float = models.FloatField(default=GAMMA)
    epsilon: float = models.FloatField(default=EPSILON)
