import datetime

from django.db import models
from django.utils import timezone

from ..base import BaseModel


class Training(BaseModel):
    """
    TODO: QUESTION: we allow nulls here to be able to migrate data from the legacy database
    """

    period = models.ForeignKey("sparta.Period", related_name="trainings", on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey("sparta.Student", related_name="trainings", on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey("sparta.Place", related_name="trainings", on_delete=models.SET_NULL, null=True)
    # start_date = models.DateField()
    # end_date = models.DateField()
    # TODO: QUESTION: can this be different to the period start date? see methods below
    # evaluation_deadline = models.DateField()  # this can be used for cases > reviews

    def is_open(self) -> bool:
        now = timezone.now()
        return now >= self.start_date and now <= self.end_date

    @property
    def start_date(self) -> datetime.date:
        return self.period.start_date

    @property
    def end_date(self) -> datetime.date:
        return self.period.end_date

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_at - self.start_at

    def accepts_cases(self) -> bool:
        raise NotImplementedError
