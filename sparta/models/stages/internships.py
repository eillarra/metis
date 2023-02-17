import datetime

from django.db import models
from django.utils import timezone
from typing import Optional

from .programmes import Programme
from ..base import BaseModel
from ..rel.remarks import RemarksMixin


class Internship(RemarksMixin, BaseModel):
    """
    An internship by a student.
    """

    period = models.ForeignKey("sparta.Period", related_name="internships", on_delete=models.CASCADE)
    student = models.ForeignKey("sparta.User", related_name="internships", on_delete=models.CASCADE)
    place = models.ForeignKey("sparta.Place", related_name="internships", on_delete=models.CASCADE)
    custom_start_date = models.DateField(null=True)  # by default start date is period's start date
    custom_end_date = models.DateField(null=True)  # by default end date is period's end date

    disciplines = models.ManyToManyField("sparta.Discipline", related_name="internships")
    # evaluation_deadline = models.DateField()  # this can be used for cases > reviews

    def clean(self) -> None:
        """
        Things to check:
        - if student has a training in the same programme (via block) check if DisciplineRule allows it
        - if Education has place rules, check if the place is allowed
        """
        return super().clean()

    @property
    def start_date(self) -> datetime.date:
        return self.custom_start_date if self.custom_start_date else self.period.start_date

    @property
    def end_date(self) -> datetime.date:
        return self.custom_end_date if self.custom_end_date else self.period.end_date

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_at - self.start_at

    @property
    def is_active(self) -> bool:
        return self.start_date <= timezone.now().date() <= self.end_date

    def accepts_cases(self) -> bool:
        raise NotImplementedError

    def programme(self) -> Optional[Programme]:
        return self.period.programme_period.programme if self.period.programme_period else None
