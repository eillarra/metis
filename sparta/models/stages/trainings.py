import datetime

from django.db import models
from django.utils import timezone

from ..base import BaseModel


class Training(BaseModel):
    period = models.ForeignKey("sparta.Period", related_name="trainings", on_delete=models.CASCADE)
    student = models.ForeignKey("sparta.Student", related_name="trainings", on_delete=models.CASCADE)
    place = models.ForeignKey("sparta.Place", related_name="trainings", on_delete=models.CASCADE)
    # start_date = models.DateField()
    # end_date = models.DateField()
    # TODO: QUESTION: can this be different to the period start date? see methods below
    evaluation_deadline = models.DateField()  # this can be used for cases > reviews

    def is_open(self) -> bool:
        now = timezone.now()
        return now >= self.start_date and now <= self.end_date

    @property
    def start_date(self) -> datetime.date:
        return self.period.start_date

    @property
    def end_date(self) -> datetime.date:
        return self.period.end_date
