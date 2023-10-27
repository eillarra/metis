from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from uuid import uuid4

from metis.models.base import BaseModel
from metis.models.rel.remarks import RemarksMixin
from metis.models.rel.signatures import SignaturesMixin


class Evaluation(RemarksMixin, SignaturesMixin, BaseModel):
    internship = models.ForeignKey("metis.Internship", related_name="evaluations", on_delete=models.CASCADE)
    form = models.ForeignKey("metis.EvaluationForm", on_delete=models.PROTECT, related_name="evaluations")
    data = models.JSONField(default=dict)
    intermediate = models.PositiveSmallIntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    class Meta:
        db_table = "metis_internship_evaluation"
        unique_together = ("internship", "intermediate")

    def clean(self) -> None:
        if self.intermediate > self.form.definition["intermediate_evaluations"]:
            raise ValidationError("Intermediate evaluation number is too high.")
        self.data = self.form.clean_response_data(self.data)
        return super().clean()

    @property
    def is_final(self) -> bool:
        return self.intermediate == 0

    def can_be_viewed_by(self, user) -> bool:
        # TODO: fix how permissions are checked
        return self.internship.student.user == user or self.internship.project.can_be_managed_by(user)

    def get_absolute_url(self) -> str:
        return reverse("evaluation_pdf", kwargs={"uuid": self.uuid})


@receiver(post_save, sender=Evaluation)
def evaluation_post_save(sender, instance, created, *args, **kwargs):
    if created:
        from metis.services.mailer import schedule_evaluation_notification

        schedule_evaluation_notification(instance)
