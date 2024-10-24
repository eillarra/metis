from datetime import date
from typing import TYPE_CHECKING
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import pgettext_lazy

from metis.models.base import BaseModel
from metis.models.rel.remarks import RemarksMixin
from metis.models.rel.signatures import SignaturesMixin


if TYPE_CHECKING:
    from metis.models.rel.signatures import Signature
    from metis.models.users import User


class Evaluation(RemarksMixin, SignaturesMixin, BaseModel):
    """An evaluation of an Internship."""

    internship = models.ForeignKey("metis.Internship", related_name="evaluations", on_delete=models.CASCADE)
    form = models.ForeignKey("metis.EvaluationForm", on_delete=models.PROTECT, related_name="evaluations")
    data = models.JSONField(default=dict)
    intermediate = models.PositiveSmallIntegerField(default=0)
    is_self_evaluation = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    class Meta:  # noqa: D106
        db_table = "metis_internship_evaluation"
        unique_together = ("internship", "intermediate", "is_self_evaluation")
        ordering = ("created_at",)

    def clean(self) -> None:
        """Validate the evaluation data using the form definition."""
        if self.is_approved:
            raise ValidationError("Cannot modify an approved evaluation.")
        if self.is_self_evaluation and not self.form.has_self_evaluations:
            raise ValidationError("This form does not support self evaluations.")
        if self.intermediate > self.form.definition["intermediate_evaluations"]:
            raise ValidationError("Intermediate evaluation number is too high.")
        self.data = self.form.clean_response_data(self.data)
        return super().clean()

    @classmethod
    def approve(cls, evaluation: "Evaluation", signature: "Signature") -> None:
        """Approve an evaluation, without calling clean() on the model. A signature is required."""
        if not signature or not signature.content_object == evaluation:
            raise ValidationError("A signature is required to approve an evaluation.")

        if not evaluation.is_approved:
            from metis.models.stages.internships import Internship
            from metis.services.mailer.evaluations import schedule_evaluation_notification

            cls.objects.filter(id=evaluation.id).update(is_approved=True)  # type: ignore

            if not evaluation.is_self_evaluation:
                # TODO: prepare extra notifications for self-evaluations
                schedule_evaluation_notification(evaluation)

            Internship.update_tags(evaluation.internship, type="evaluations")

    @property
    def is_final(self) -> bool:
        """Boolean indicating whether this is the final evaluation."""
        return self.intermediate == 0

    @property
    def name(self) -> str:
        """Evaluation name or type."""
        final_name = (
            pgettext_lazy("evaluations.Evaluation.name", "Final self-evaluation")
            if self.is_self_evaluation
            else pgettext_lazy("evaluations.Evaluation.name", "Final evaluation")
        )
        intermediate_name = (
            pgettext_lazy("evaluations.Evaluation.name", "Intermediate self-evaluation #%(num)d")
            if self.is_self_evaluation
            else pgettext_lazy("evaluations.Evaluation.name", "Intermediate evaluation #%(num)d")
        )

        return final_name if self.is_final else intermediate_name % {"num": self.intermediate}

    @property
    def evaluation_periods(self) -> list[tuple[int, date, date]]:
        """The evaluation periods for the associated internship."""
        return self.internship.get_evaluation_periods(self.form)

    def can_be_viewed_by(self, user: "User") -> bool:
        """Return whether the user can view this evaluation."""
        return self.internship.can_be_viewed_by(user)

    def get_absolute_url(self) -> str:
        """Return the absolute URL of the evaluation PDF."""
        return reverse("evaluation_pdf", kwargs={"uuid": self.uuid})


@receiver(post_save, sender=Evaluation)
def post_save_evaluation(sender, instance, **kwargs):
    """Update the evaluation tags of the associated internship when an evaluation is saved."""
    sync_evaluation_tags(instance)


@receiver(post_delete, sender=Evaluation)
def post_delete_evaluation(sender, instance, **kwargs):
    """Update the evaluation tags of the associated internship when an evaluation is deleted."""
    sync_evaluation_tags(instance)


def sync_evaluation_tags(instance):
    """Sync the evaluation tags of the associated internship."""
    from metis.models.stages.internships import Internship

    Internship.update_tags(instance.internship, type="evaluations")
