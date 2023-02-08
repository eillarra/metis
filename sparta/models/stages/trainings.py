import datetime

from django.db import models
from django.utils import timezone

from ..base import BaseModel
from ..rel.remarks import RemarksMixin


class Training(RemarksMixin, BaseModel):
    """
    TODO: QUESTION: we allow nulls here to be able to migrate data from the legacy database
    If we are not migrating existing data, or not all of it, we should remove the nulls
    """

    block = models.ForeignKey("sparta.ProgrammeBlock", related_name="trainings", on_delete=models.SET_NULL, null=True)
    period = models.ForeignKey("sparta.Period", related_name="trainings", on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey("sparta.User", related_name="trainings", on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey("sparta.Place", related_name="trainings", on_delete=models.SET_NULL, null=True)
    custom_start_date = models.DateField(null=True)  # by default start date is period's start date
    custom_end_date = models.DateField(null=True)  # by default end date is period's end date

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

    def is_active(self) -> bool:
        today = timezone.now().date()
        return today >= self.start_date and today <= self.end_date

    def accepts_cases(self) -> bool:
        raise NotImplementedError
