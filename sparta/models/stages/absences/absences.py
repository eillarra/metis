from django.core.exceptions import ValidationError
from django.db import models

from sparta.models.base import BaseModel
from sparta.models.rel.files import FilesMixin
from sparta.models.rel.remarks import RemarksMixin


class Absence(FilesMixin, RemarksMixin, BaseModel):
    """
    TODO: QUESTION: currently these are linked to projects? does it make any sense? it should be linked to trainings
    """

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    STATUSES = (
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    )

    training = models.ForeignKey("sparta.Training", related_name="absences", on_delete=models.SET_NULL, null=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=8, choices=STATUSES, default=PENDING)

    class Meta:
        db_table = "sparta_training_absence"

    def clean(self) -> None:
        """
        TODO: QUESTION: training should be required and removed from the conditions below
        """
        if self.training and self.start_at < self.training.period.start_at:
            raise ValidationError("Absence start date cannot be before training start date.")

        if self.training and self.end_at > self.training.period.end_at:
            raise ValidationError("Absence end date cannot be after training end date.")

    @property
    def day_count(self) -> float:
        return (self.end_at - self.start_at).hours / 24
