import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from typing import Optional

from ..base import BaseModel


class Project(BaseModel):
    education = models.ForeignKey("sparta.Education", null=True, related_name="projects", on_delete=models.SET_NULL)
    name = models.CharField(max_length=160)

    is_active = models.BooleanField(default=True)
    is_visible_to_planner = models.BooleanField(default=True)
    is_visible_to_contacts = models.BooleanField(default=True)
    is_visible_to_students = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    @cached_property
    def start_date(self) -> Optional[datetime.date]:
        return self.periods.first().start_date if self.periods.exists() else None

    @cached_property
    def end_date(self) -> Optional[datetime.date]:
        return self.periods.last().end_date if self.periods.exists() else None

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_at - self.start_at

    @property
    def is_open(self) -> bool:
        return (
            self.is_active
            and self.start_date
            and self.end_date
            and (self.start_date < timezone.now().date() < self.end_date)
        )


class Period(BaseModel):
    project = models.ForeignKey(Project, related_name="periods", on_delete=models.CASCADE)
    name = models.CharField(max_length=240)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = "sparta_project_period"
        ordering = ["project", "start_date"]

    def clean(self) -> None:
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")

        return super().clean()

    @property
    def is_open(self) -> bool:
        return self.is_active and self.start_date < timezone.now().date() < self.end_date

    def accepts_cases(self, *, extension_days: int = 4) -> bool:
        """
        De casus wordt 'automatisch' gekoppeld aan een stage. De uiterste indiendatum kan per project ingesteld worden (Dit wordt ingesteld op niveau van het 'Casustype', analoog aan de instellingen van de datums voor beoordeling stages), typisch is deze uiterste datum relatief tov einddatum van de stage van de student. (De einddatum van de stage van een student valt mogelijks niet samen met een blokgrens.)
        """
        return self.is_open or self.end_date + timezone.timedelta(days=extension_days) < timezone.now().date()
