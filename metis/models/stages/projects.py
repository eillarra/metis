import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from ..base import BaseModel


class Project(BaseModel):
    """
    A project is a collection of internships for an academic year or other period of time.
    Projects are created so that the planner can distribute students to places. It is mainly an administrative tool.
    """

    education = models.ForeignKey("metis.Education", null=True, related_name="projects", on_delete=models.SET_NULL)
    name = models.CharField(max_length=160)

    is_active = models.BooleanField(default=True)
    is_visible_to_planner = models.BooleanField(default=True)
    is_visible_to_contacts = models.BooleanField(default=True)
    is_visible_to_students = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    @cached_property
    def start_date(self) -> datetime.date:
        return self.periods.first().start_date

    @cached_property
    def end_date(self) -> datetime.date:
        return self.periods.last().end_date

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_at - self.start_at

    @property
    def is_open(self) -> bool:
        return self.is_active and self.periods.exists() and (self.start_date <= timezone.now().date() <= self.end_date)

    def can_be_managed_by(self, user) -> bool:
        return self.education.can_be_managed_by(user)


class Period(BaseModel):
    """
    A first proposal is made based on the ProgramInternships defined at ProgramBlock level.
    """

    project = models.ForeignKey(Project, related_name="periods", on_delete=models.CASCADE)
    program_internship = models.ForeignKey(
        "metis.ProgramInternship", null=True, related_name="project_periods", on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=240)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = "metis_project_period"
        ordering = ["project", "start_date"]

    def clean(self) -> None:
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")

        return super().clean()

    @property
    def is_open(self) -> bool:
        return self.is_active and (self.start_date <= timezone.now().date() <= self.end_date)

    def accepts_cases(self, *, extension_days: int = 4) -> bool:
        """
        De casus wordt 'automatisch' gekoppeld aan een stage. De uiterste indiendatum kan per project ingesteld worden
        (Dit wordt ingesteld op niveau van het 'Casustype', analoog aan de instellingen van de datums voor beoordeling
        stages), typisch is deze uiterste datum relatief tov einddatum van de stage van de student. (De einddatum van
        de stage van een student valt mogelijks niet samen met een blokgrens.)
        """
        return self.is_open or (self.end_date + timezone.timedelta(days=extension_days) < timezone.now().date())