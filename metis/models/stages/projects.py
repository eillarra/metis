import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from typing import Optional, TYPE_CHECKING

from ..base import BaseModel
from ..rel import TextEntriesMixin

if TYPE_CHECKING:
    from ..rel import TextEntry


class Project(TextEntriesMixin, BaseModel):
    """
    A project is a collection of internships for an academic year or other period of time.
    Projects are created so that the planner can distribute students to places. It is mainly an administrative tool.
    """

    education = models.ForeignKey("metis.Education", related_name="projects", on_delete=models.PROTECT)
    program = models.ForeignKey("metis.Program", related_name="projects", on_delete=models.PROTECT)
    name = models.CharField(max_length=32)

    is_active = models.BooleanField(default=True)
    is_visible_to_planner = models.BooleanField(default=True)
    is_visible_to_contacts = models.BooleanField(default=True)
    is_visible_to_students = models.BooleanField(default=False)

    places = models.ManyToManyField("metis.Place", through="metis.ProjectPlace")

    # TODO: QUESTION: there are dates in the old database, do we need them or do we use the period/project dates?

    # number_of_periods = ???
    # min_place_choices
    # max_place_choices
    # min_region_choices
    # max_region_choices
    # dates: select_period,

    def clean(self) -> None:
        if self.program.education != self.education:
            raise ValidationError("Choose a program from the same education")

        return super().clean()

    def __str__(self) -> str:
        return self.name

    def can_be_managed_by(self, user) -> bool:
        return self.education.can_be_managed_by(user)

    @property
    def full_name(self) -> str:
        return f"{self.education.name} - {self.name}"

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

    @property
    def internship_agreement(self) -> Optional["TextEntry"]:
        return self.get_text("project.internship_agreement")


class Period(BaseModel):
    """
    A first proposal is made based on the ProgramInternships defined at ProgramBlock level.
    """

    project = models.ForeignKey(Project, related_name="periods", on_delete=models.CASCADE)
    program_internship = models.ForeignKey(
        "metis.ProgramInternship", null=True, related_name="periods", on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=240)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = "metis_project_periods"
        ordering = ["project", "start_date"]
        unique_together = ["project", "program_internship"]

    def clean(self) -> None:
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")
        if self.program_internship.block.program != self.project.program:
            raise ValidationError("Choose a program internship from the project program")

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
