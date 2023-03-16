from collections import Counter
from django.db import models
from django.utils import timezone
from typing import List, Optional

from ..base import BaseModel
from ..disciplines import Discipline
from .constraints import DisciplineConstraint, DisciplineConstraintsMixin


class Program(DisciplineConstraintsMixin, BaseModel):
    """
    A generic definition of an internship curriculum.
    Different constraints can be applied to the program.
    Constraints: cannot repeat place
    Choice of disciplines: can be repeated

    How many places can the student choose prefernecse
    How many regions can the student choose preferences
    """

    education = models.ForeignKey("sparta.Education", related_name="Programs", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    valid_from = models.DateField()
    valid_until = models.DateField(null=True, blank=True)

    # evaluation_form = models.ForeignKey("sparta.EvaluationForm", related_name="Programs", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.education} - {self.name}"

    @property
    def is_valid(self):
        today = timezone.now().date()
        return self.valid_from <= today and (not self.valid_until or self.valid_until >= today)


class ProgramBlock(DisciplineConstraintsMixin, BaseModel):
    """
    Based on semesters or a natural year, a orientative block is defined.
    Normally these will be linked to an academic year, and they will be closely related to degrees (Ba3, Ma1, Ma2).
    """

    program = models.ForeignKey(Program, related_name="blocks", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "sparta_program_block"
        unique_together = ("program", "position")
        ordering = ["program", "position"]

    def __str__(self) -> str:
        return f"{self.program} - {self.name}"


class ProgramInternship(DisciplineConstraintsMixin, BaseModel):
    """
    An internship inside a ProgramBlock.
    The final Internship or stage will be linked to this model, so we can later check the dependencies
    and make sure the student has covered all the requirements for the Program / Track.
    A ProgramInternship defines some orientative 'dates' that will be used to create the actual
    internship periods for a Project.

    Extra constraints:
    - How many places can the student choose prefernecse
    - Choose place regions
    - Preferences for disciplines (ordered or unordered)
    """

    block = models.ForeignKey(ProgramBlock, related_name="internships", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)
    start_week = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        db_table = "sparta_program_internship"
        ordering = ["block", "position"]

    def __str__(self) -> str:
        return f"{self.block} - {self.name}"

    def add_required_discipline(self, discipline: Discipline) -> None:
        constraint = self.constraints.create(min_count=1, max_count=1, max_repeat=1)
        constraint.disciplines.set([discipline])

    def get_remaining_discipline_constraints(
        self, covered_discipline_ids: List[int], *, track: Optional["Track"] = None
    ) -> List[DisciplineConstraint]:
        """
        Calculate the remaining discipline constraints based on the initial constraints of the track or the internship
        and the disciplines already covered by the student.

        Args:
            covered_discipline_ids (List[int]): A list of discipline IDs already covered by the student.

        Returns:
            List[DisciplineConstraint]: A list of remaining DisciplineConstraint objects.
        """

        covered_counts = Counter(covered_discipline_ids)
        remaining_constraints = []

        constraints = self.constraints.all()

        if track:
            internship_ids_in_track = track.internships.values_list("id", flat=True)
            constraints = [constraint for constraint in constraints if constraint.object_id in internship_ids_in_track]

        for constraint in constraints:
            remaining_min_count = max(
                constraint.min_count
                - sum(
                    covered_counts[discipline_id]
                    for discipline_id in constraint.disciplines.values_list("id", flat=True)
                ),
                0,
            )

            remaining_max_count = None
            if constraint.max_count is not None:
                remaining_max_count = max(
                    constraint.max_count
                    - sum(
                        covered_counts[discipline_id]
                        for discipline_id in constraint.disciplines.values_list("id", flat=True)
                    ),
                    0,
                )

            remaining_max_repeat = None
            if constraint.max_repeat is not None:
                remaining_max_repeat = constraint.max_repeat - max(
                    covered_counts.get(discipline_id, 0)
                    for discipline_id in constraint.disciplines.values_list("id", flat=True)
                )

            remaining_constraint = DisciplineConstraint(
                content_object=constraint.content_object,
                min_count=remaining_min_count,
                max_count=remaining_max_count,
                max_repeat=remaining_max_repeat,
            )
            remaining_constraint.disciplines.set(constraint.disciplines.all())
            remaining_constraints.append(remaining_constraint)

        return remaining_constraints


class Track(DisciplineConstraintsMixin, BaseModel):
    """
    A Track is a set of program internships that are related and (can) have some constraints of their own.
    """

    program = models.ForeignKey(Program, related_name="tracks", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    internships = models.ManyToManyField(ProgramInternship, through="TrackInternship")

    class Meta:
        db_table = "sparta_program_track"

    def __str__(self) -> str:
        return f"{self.program} - {self.name}"

    @property
    def is_available(self) -> bool:
        return self.program.is_valid


class TrackInternship(DisciplineConstraintsMixin, models.Model):
    """
    Related model that defines the order of the internships inside a Track.
    Special requirements for a Track are also saved here.
    """

    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    internship = models.ForeignKey(ProgramInternship, related_name="tracks", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "sparta_program_track_internship"
        ordering = ["track", "position"]
