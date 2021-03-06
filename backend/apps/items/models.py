from django.db import models
from django.contrib.postgres.fields import JSONField
from backend.fields import ShortUUIDField
from backend.celery import app as celery_app
from apps.surveys.models import Survey
from apps.crowd_bt.constants import MU, SIGMA_SQUARED
from apps.crowd_bt.types import Mu, SigmaSquared, RelevanceScore
from .tasks import auto_deactivate


class Item(models.Model):
    uuid: str = ShortUUIDField()
    name: str = models.CharField(max_length=30)
    metadata = JSONField(default=dict)
    active: bool = models.BooleanField(default=False)
    prioritized: bool = models.BooleanField(default=False)
    survey: Survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="items"
    )

    mu: Mu = models.FloatField(default=MU)
    sigma_squared: SigmaSquared = models.FloatField(default=SIGMA_SQUARED)

    @property
    def score(self) -> RelevanceScore:
        return RelevanceScore(self.mu, self.sigma_squared)

    @property
    def auto_deactivate_task_id(self) -> str:
        current_annotator_uuid = self.current_annotators.only("uuid").first().uuid
        return f"auto_deactivate_{self.uuid}_{current_annotator_uuid}"

    def prioritize(self) -> None:
        self.prioritized = True
        self.save()

    def deprioritize(self) -> None:
        self.prioritized = False
        self.save()

    def activate(self) -> None:
        self.active = True
        self.save()

    def deactivate(self) -> None:
        self.active = False
        self.save()
        # Cancel auto deactivation tasks
        celery_app.control.revoke(self.auto_deactivate_task_id)

    def update_score(self, new_score: RelevanceScore) -> None:
        self.mu = new_score.mu  # pylint: disable=invalid-name
        self.sigma_squared = new_score.sigma_squared
        self.save()

    def schedule_deactivate(self, max_time: int) -> None:
        if max_time > 0:
            auto_deactivate.apply_async(
                (self.pk,), countdown=max_time, task_id=self.auto_deactivate_task_id
            )
