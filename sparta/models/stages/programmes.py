from django.db import models
from django.utils import timezone

from ..base import BaseModel


class Programme(BaseModel):
    """
    A generic definition of an internship curriculum.
    """

    education = models.ForeignKey("sparta.Education", related_name="programmes", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    valid_from = models.DateField()
    valid_until = models.DateField(null=True, blank=True)

    # evaluation_form = models.ForeignKey("sparta.EvaluationForm", related_name="programmes", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.education} - {self.name}"

    @property
    def is_valid(self) -> bool:
        return self.valid_from <= timezone.now().date() <= self.valid_until


class ProgrammeBlock(BaseModel):
    """
    Based on semesters or a natural year, a orientative block is defined.
    Normally these will be linked to an academic year, and they will be closely related to degrees (Ba3, Ma1, Ma2).
    """

    programme = models.ForeignKey(Programme, related_name="blocks", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "sparta_programme_block"
        unique_together = ("programme", "position")
        ordering = ["programme", "position"]

    def __str__(self) -> str:
        return f"{self.programme} - {self.name}"


class ProgrammePeriod(BaseModel):
    """
    An internship period inside a ProgrammeBlock.
    The final internships or stages will be linked to this model, so we can later check the dependencies
    between them and make sure the student has covered all the requirements for the programme.
    A programme period defines some orientative 'dates' that will be used to create the actual periods for a project.
    TODO: can we reach this via Internship => Period => ProgrammePeriod? Maybe remove programme_period from Internship?
    """

    block = models.ForeignKey(ProgrammeBlock, related_name="periods", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)
    start_week = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        db_table = "sparta_programme_period"
        ordering = ["block", "position"]

    def __str__(self) -> str:
        return f"{self.block} - {self.name}"


class Trajectory(BaseModel):
    """
    A trajectory is a set of periods that are related and have some kind of dependency.
    """

    name = models.CharField(max_length=160)
    periods = models.ManyToManyField(ProgrammePeriod, through="TrajectoryPeriod")

    class Meta:
        db_table = "sparta_programme_trajectory"

    def __str__(self) -> str:
        return f"{self.programme} - {self.name}"


class TrajectoryPeriod(BaseModel):
    """
    Related model that defines the order of the periods inside a trajectory.
    """

    trajectory = models.ForeignKey(Trajectory, on_delete=models.CASCADE)
    period = models.ForeignKey(ProgrammePeriod, related_name="trajectories", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "sparta_programme_trajectory_period"
        ordering = ["trajectory", "position"]


class DisciplineRule(BaseModel):
    REQUIRED = "required"
    OPTIONAL = "optional"
    TYPES = (
        (REQUIRED, "Required"),
        (OPTIONAL, "Optional"),
    )

    programme = models.ForeignKey(Programme, related_name="discipline_rules", on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=TYPES, default=REQUIRED)
    disciplines = models.ManyToManyField("sparta.Discipline", related_name="rules")
    choices = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["programme", "type"]
        unique_together = ("programme", "type")

    """
    there is sometimes a project that is not part of the programme,+
    that takes the space of a period
    """

    def clean(self) -> None:
        pass

    """
    other rules: what period should be used
    """
