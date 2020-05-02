from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.surveys.models import Survey
from crowd_bt.constants import MU, SIGMA_SQUARED
from crowd_bt.types import Mu, SigmaSquared, RelevanceScore


class Item(models.Model):
    name: str = models.CharField(max_length=30)
    metadata = JSONField()
    active: bool = models.BooleanField(default=False)
    prioritized: bool = models.BooleanField(default=False)
    survey: Survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="items"
    )

    mu: Mu = models.FloatField(default=MU)
    sigma_squared: SigmaSquared = models.FloatField(default=SIGMA_SQUARED)

    @property
    def score(self):
        return RelevanceScore(self.mu, self.sigma_squared)

    def prioritize(self):
        self.prioritized = True
        self.save()

    def deprioritize(self):
        self.prioritized = True
        self.save()

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def update_score(self, new_score: RelevanceScore):
        self.mu = new_score.mu
        self.sigma_squared = new_score.sigma_squared
        self.save()
