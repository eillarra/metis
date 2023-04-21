from django.core.exceptions import ValidationError
from django.db import models

from metis.models.base import BaseModel
from metis.models.rel.files import FilesMixin
from metis.models.rel.remarks import RemarksMixin


class Absence(FilesMixin, RemarksMixin, BaseModel):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    STATUSES = (
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    )

    internship = models.ForeignKey("metis.Internship", related_name="absences", on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=8, choices=STATUSES, default=PENDING)

    class Meta:
        db_table = "metis_internship_absence"

    def clean(self) -> None:
        if self.start_at.date() < self.training.start_date:
            raise ValidationError("Absence start date cannot be before training start date.")

        if self.end_at.date() > self.training.end_date:
            raise ValidationError("Absence end date cannot be after training end date.")

    @property
    def day_count(self) -> float:
        return (self.end_at - self.start_at).hours / 24
