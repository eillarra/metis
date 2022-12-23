import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from ..base import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=255)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    disciplines = models.ManyToManyField("sparta.Discipline", related_name="projects")

    is_visible_to_planner = models.BooleanField(default=True)
    is_visible_to_contacts = models.BooleanField(default=True)
    is_visible_to_students = models.BooleanField(default=False)
    # IsVisibleForBureau

    def __str__(self) -> str:
        return self.name

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_at - self.start_at

    @property
    def is_open(self) -> bool:
        return self.is_active and self.start_at < timezone.now() < self.end_at


class Period(BaseModel):
    project = models.ForeignKey(Project, related_name="periods", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = "sparta_project_period"

    def clean(self) -> None:
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")

        if self.project.start_at.date() > self.start_date:
            raise ValidationError("Period start date must be after project start date.")

        if self.project.end_at.date() < self.end_date:
            raise ValidationError("Period end date must be before project end date.")

        return super().clean()

    @property
    def is_open(self) -> bool:
        return self.is_active and self.start_date < timezone.now().date() < self.end_date

    def accepts_cases(self, *, extension_days: int = 4) -> bool:
        """
        De casus wordt 'automatisch' gekoppeld aan een stage. De uiterste indiendatum kan per project ingesteld worden (Dit wordt ingesteld op niveau van het 'Casustype', analoog aan de instellingen van de datums voor beoordeling stages), typisch is deze uiterste datum relatief tov einddatum van de stage van de student. (De einddatum van de stage van een student valt mogelijks niet samen met een blokgrens.)
        """
        return self.is_open or self.end_date + timezone.timedelta(days=extension_days) < timezone.now().date()
