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
    between them and make sure the student has covered all the requirements for the programme / trajectory.
    A programme period defines some orientative 'dates' that will be used to create the actual periods for a project.
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
    A trajectory is a set of periods that are related and have some dependencies defined.
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
    Special requirements for a trajectory are also saved here.
    """

    trajectory = models.ForeignKey(Trajectory, on_delete=models.CASCADE)
    period = models.ForeignKey(ProgrammePeriod, related_name="trajectories", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "sparta_programme_trajectory_period"
        ordering = ["trajectory", "position"]
