import datetime

from collections import Counter
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from typing import List, Optional, TYPE_CHECKING

from ..base import BaseModel
from ..disciplines import Discipline
from ..rel.remarks import RemarksMixin
from .projects import Project

if TYPE_CHECKING:
    from ..places import Place
    from .programs import Program


def get_remaining_discipline_constraints(obj: "Internship") -> List[dict]:
    """
    Calculate the remaining discipline constraints based on the track constraints.

    Args:
        obj (Internship): An instance of the Internship class.

    Returns:
        List[Dict]: A list of remaining DisciplineConstraint objects.
    """

    covered_counts = obj.get_counter_for_disciplines()
    remaining_constraints = []

    # check internship contraints

    if obj.track:
        for constraint in obj.track.constraints.all():
            constraint_discipline_ids = list(constraint.disciplines.values_list("id", flat=True))
            remaining_min_count = constraint.min_count
            remaining_max_count = constraint.max_count
            remaining_max_repeat = constraint.max_repeat

            for discipline_id, count in covered_counts.items():
                if discipline_id in constraint_discipline_ids:
                    remaining_min_count = remaining_min_count - count
                    remaining_max_count = remaining_max_count - count
                    remaining_max_repeat = remaining_max_repeat - 1

            remaining_constraint = {
                "min_count": max(0, remaining_min_count),
                "max_count": max(0, remaining_max_count),
                "max_repeat": max(0, remaining_max_repeat),
                "disciplines": constraint.disciplines.all(),
            }

            remaining_constraints.append(remaining_constraint)

    return remaining_constraints


def validate_discipline_choice(obj: "Internship") -> None:
    """
    TODO: this needs refactoring.
    """
    """
    Validate if the chosen discipline for an internship is available and meets the constraints.

    This function checks whether the chosen discipline is one of the available disciplines
    for the given internship program, and if it meets the remaining constraints for the student.
    Raises a ValidationError if the chosen discipline is invalid.

    Args:
        obj (Internship): An instance of the Internship class.

    Raises:
        ValidationError: If the chosen discipline is not available for the internship program
            or does not meet the remaining constraints for the student.

    Example:
        validate_discipline_choice(my_internship)
    """
    if obj.discipline not in obj.get_available_disciplines():
        raise ValidationError(f"Chosen discipline is not available for this internship: {obj.program_internship}")

    if obj.track and obj.get_counter_for_disciplines()[obj.discipline_id] >= obj.track.constraints.first().max_repeat:
        raise ValidationError("Chosen discipline does not meet the remaining constraints for this internship.")

    for constraint in get_remaining_discipline_constraints(obj):
        if constraint["max_count"] == 0:
            raise ValidationError("Chosen discipline does not meet the remaining constraints for this internship.")


class Internship(RemarksMixin, BaseModel):
    """
    An internship by a student.
    """

    # TODO: change to Period relation
    program_internship = models.ForeignKey(
        "metis.ProgramInternship", related_name="internships", on_delete=models.CASCADE
    )
    track = models.ForeignKey("metis.Track", related_name="internships", null=True, on_delete=models.SET_NULL)

    student = models.ForeignKey("metis.Student", related_name="internships", null=True, on_delete=models.SET_NULL)
    project_place = models.ForeignKey("metis.ProjectPlace", related_name="internships", on_delete=models.PROTECT)
    custom_start_date = models.DateField(null=True)  # by default start date is period's start date
    custom_end_date = models.DateField(null=True)  # by default end date is period's end date

    discipline = models.ForeignKey("metis.Discipline", related_name="internships", null=True, on_delete=models.SET_NULL)
    # evaluation_deadline = models.DateField()  # this can be used for cases > reviews
    # mentors

    def clean(self) -> None:
        """
        Things to check:
        - the selected program_internship is part of the selected track (if a track is selected)
        - the place is one of the places available for the Project (via track)
        - if the student has previous internships in same Track, check if DisciplineConstraint allows it
        - TODO: if Education has place rules, check if the place is allowed
        """
        if self.student and self.project_place not in self.student.project.place_set.all():
            raise ValidationError("The chosen place is not part of the chosen project.")
        if self.track and not self.track.program_internships.filter(id=self.program_internship.id).count():
            raise ValidationError("The chosen program internship is not part of the chosen track.")

        validate_discipline_choice(self)
        return super().clean()

    @cached_property
    def place(self) -> "Place":
        return self.project_place.place

    @property
    def start_date(self) -> datetime.date:
        return self.custom_start_date if self.custom_start_date else self.period.start_date

    @property
    def end_date(self) -> datetime.date:
        return self.custom_end_date if self.custom_end_date else self.period.end_date

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_at - self.start_at

    @property
    def is_active(self) -> bool:
        return self.start_date <= timezone.now().date() <= self.end_date

    @property
    def program(self) -> Optional["Program"]:
        return self.program_internship.block.program if self.period.program_period else None

    @property
    def project(self) -> Optional["Project"]:
        return self.student.project if self.student else None

    def accepts_cases(self) -> bool:
        raise NotImplementedError

    def get_available_disciplines(self) -> models.QuerySet:
        """
        Returns a set of all available disciplines included in the constraints.

        Returns:
            QuerySet: A QuerySet of Discipline objects.
        """
        program_disciplines = self.program_internship.get_available_disciplines()

        if program_disciplines.count() > 0:
            return program_disciplines

        return self.track.get_available_disciplines() if self.track else Discipline.objects.none()

    def get_covered_disciplines(self) -> models.QuerySet:
        """
        If a track exists, it returns a list of disciplines that have already been covered by this student.

        Returns:
            QuerySet: A QuerySet of Discipline objects.
        """
        if self.track is None or self.student is None:
            return Discipline.objects.none()

        past_internships = self.student.internships.exclude(id=self.id).filter(track=self.track)
        return Discipline.objects.filter(internships__in=past_internships)

    def get_counter_for_disciplines(self) -> Counter:
        """
        Returns a dictionary of discipline IDs and their count for this internship.

        Returns:
            Dict: A dictionary of disciplines and their count for this internship.
        """
        if not self.track:
            return Counter()

        return Counter(self.get_covered_disciplines().values_list("id", flat=True))
