from datetime import time
from django.core.exceptions import ValidationError
from django.db import models
from typing import TYPE_CHECKING

from metis.models.base import BaseModel
from metis.models.rel.files import FilesMixin
from metis.models.rel.remarks import RemarksMixin
from metis.utils.dates import get_minutes_difference, get_time_difference, sum_times

if TYPE_CHECKING:
    from ..rel.signatures import Signature


class Absence(FilesMixin, RemarksMixin, BaseModel):
    """
    An absence during a student's internship.
    """

    internship = models.ForeignKey("metis.Internship", related_name="absences", on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_approved = models.BooleanField(default=None, null=True, blank=True)

    class Meta:
        db_table = "metis_internship_absence"

    def clean(self) -> None:
        if self.start_at.date() < self.internship.start_date:
            raise ValidationError("Absence start date cannot be before internship start date.")

        if self.end_at.date() > self.internship.end_date:
            raise ValidationError("Absence end date cannot be after internship end date.")

    @classmethod
    def approve(cls, absence: "Absence", signature: "Signature") -> None:
        """Approve an absence, without calling clean() on the model. A signature is required."""
        if not signature or not signature.content_object == absence:
            raise ValidationError("A signature is required to approve an absence.")
        cls.objects.filter(id=absence.pk).update(is_approved=True)


class Timesheet(BaseModel):
    """
    A timesheet for a student during their internship.
    At least one of the time field "couples" must be filled in (am or pm).
    """

    internship = models.ForeignKey("metis.Internship", related_name="timesheets", on_delete=models.CASCADE)
    date = models.DateField()
    start_time_am = models.TimeField(null=True, blank=True)
    end_time_am = models.TimeField(null=True, blank=True)
    start_time_pm = models.TimeField(null=True, blank=True)
    end_time_pm = models.TimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = "metis_internship_timesheet"
        unique_together = (("internship", "date"),)

    def clean(self) -> None:
        if self.date < self.internship.start_date or self.date > self.internship.end_date:
            raise ValidationError("Timesheet date must be within internship start and end dates.")
        if not self.start_time_am and not self.start_time_pm and not self.end_time_am and not self.end_time_pm:
            raise ValidationError("At least one of the time field couples must be filled in (am or pm).")
        if self.start_time_am and not self.end_time_am:
            raise ValidationError("If start_time_am is filled in, end_time_am must be filled in as well.")
        if not self.start_time_am and self.end_time_am:
            raise ValidationError("If end_time_am is filled in, start_time_am must be filled in as well.")
        if self.start_time_pm and not self.end_time_pm:
            raise ValidationError("If start_time_pm is filled in, end_time_pm must be filled in as well.")
        if not self.start_time_pm and self.end_time_pm:
            raise ValidationError("If end_time_pm is filled in, start_time_pm must be filled in as well.")
        if self.start_time_pm and self.end_time_am and self.start_time_pm < self.end_time_am:
            raise ValidationError("start_time_pm cannot be before end_time_am.")
        if self.start_time_am and self.end_time_am and self.end_time_am <= self.start_time_am:
            raise ValidationError("end_time_am cannot be before or equal to start_time_am.")
        if self.start_time_pm and self.end_time_pm and self.end_time_pm <= self.start_time_pm:
            raise ValidationError("end_time_pm cannot be before or equal to start_time_pm.")
        if (
            self.start_time_pm
            and self.end_time_am
            and get_minutes_difference(self.start_time_pm, self.end_time_am) < 30
        ):
            raise ValidationError("The difference between start_time_pm and end_time_am must be at least 30 minutes.")

    @classmethod
    def approve(cls, timesheet: "Timesheet", signature: "Signature") -> None:
        """Approve a timesheet, without calling clean() on the model. A signature is required."""
        if not signature or not signature.content_object == timesheet:
            raise ValidationError("A signature is required to approve a timesheet.")
        cls.objects.filter(id=timesheet.pk).update(is_approved=True)

    @property
    def duration(self) -> time:
        """
        return duration as dateime.time for the total hours worked on the timesheet
        """
        am_diff = time(0, 0)
        pm_diff = time(0, 0)

        if self.start_time_am and self.end_time_am:
            am_diff = get_time_difference(self.start_time_am, self.end_time_am)
        if self.start_time_pm and self.end_time_pm:
            pm_diff = get_time_difference(self.start_time_pm, self.end_time_pm)

        return sum_times([am_diff, pm_diff])
