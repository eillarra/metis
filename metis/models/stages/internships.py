import math
from collections import Counter
from typing import TYPE_CHECKING, Optional

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from metis.utils.dates import sum_times

from ..base import BaseModel
from ..disciplines import Discipline
from ..rel.remarks import RemarksMixin


if TYPE_CHECKING:
    from ..places import Place
    from .evaluations import EvaluationForm
    from .programs import Program


def get_remaining_discipline_constraints(obj: "Internship") -> list[dict]:
    """Calculate the remaining discipline constraints based on the track constraints.

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
            remaining_max_count = constraint.max_count or math.inf
            remaining_max_repeat = constraint.max_repeat or math.inf

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
    """TODO: this needs refactoring."""
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
        raise ValidationError(
            f"Chosen discipline is not available for this internship: {obj.period.program_internship}"
        )

    if obj.track:
        max_repeat = obj.track.constraints.first().max_repeat
        if max_repeat and obj.get_counter_for_disciplines()[obj.discipline_id] >= max_repeat:
            raise ValidationError(
                "Chosen discipline does not meet the remaining constraints for this internship: "
                f"{obj.track}, {obj.student}"
            )

    for constraint in get_remaining_discipline_constraints(obj):
        if constraint["max_count"] == 0:
            raise ValidationError("Chosen discipline does not meet the remaining constraints for this internship.")


class Internship(RemarksMixin, BaseModel):
    """An internship for a student."""

    PREPLANNING = "preplanning"
    CONCEPT = "concept"
    DEFINITIVE = "definitive"
    CANCELLED = "cancelled"
    UNSUCCESSFUL = "unsuccessful"
    STATUS_CHOICES = [
        (PREPLANNING, "Preplanning"),
        (CONCEPT, "Concept"),
        (DEFINITIVE, "Definitive"),
        (CANCELLED, "Cancelled"),
        (UNSUCCESSFUL, "Unsuccessful"),
    ]

    project = models.ForeignKey("metis.Project", related_name="internships", on_delete=models.PROTECT)
    period = models.ForeignKey("metis.Period", related_name="internships", null=True, on_delete=models.SET_NULL)
    track = models.ForeignKey("metis.Track", related_name="internships", null=True, on_delete=models.SET_NULL)

    student = models.ForeignKey("metis.Student", related_name="internships", null=True, on_delete=models.PROTECT)
    project_place = models.ForeignKey("metis.ProjectPlace", related_name="internships", on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()

    discipline = models.ForeignKey("metis.Discipline", related_name="internships", null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CONCEPT)

    # evaluation_deadline = models.DateField()  # this can be used for cases > reviews
    # reviewers (beoordelaars)

    def clean(self) -> None:
        """Validate the internship data.

        Things to check:
        - the place is one of the places available for the project
        - the selected student is part of the selected project
        - the selected period is part of the selected project
        - the selected period.program_internship is part of the selected track (if a track is selected)
        - the dates are within the selected period, and valid
        - if the student has previous internships in same Track, check if DisciplineConstraint allows it
        - TODO: if Education has place rules, check if the place is allowed
        """
        if self.student and self.student.project_id != self.project_id:
            raise ValidationError("The chosen student is not part of the chosen project.")
        if self.period and self.period.project_id != self.project_id:
            raise ValidationError("The chosen period is not part of the chosen project.")
        if self.project_place and self.project_place.project_id != self.project_id:
            raise ValidationError("The chosen place is not part of the chosen project.")
        if self.track and not self.track.program_internships.filter(id=self.period.program_internship_id).count():
            raise ValidationError("The chosen program internship is not part of the chosen track.")
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("The chosen start date is after the chosen end date.")

        validate_discipline_choice(self)
        return super().clean()

    def save(self, *args, **kwargs) -> None:
        if not self.pk and self.period:
            if not self.start_date:
                self.start_date = self.period.start_date
            if not self.end_date:
                self.end_date = self.period.end_date
        super().save(*args, **kwargs)

    def can_be_managed_by(self, user) -> bool:
        return self.project.can_be_managed_by(user)

    @property
    def is_active(self) -> bool:
        """A boolean indicating whether the internship is active or not."""
        return self.start_date <= timezone.now().date() <= self.end_date

    @property
    def evaluation_form(self) -> Optional["EvaluationForm"]:
        """The evaluation form for this internship."""
        qs = self.project.evaluation_forms.all()

        if self.period and qs.filter(period=self.period).exists():
            qs = self.period.evaluation_forms.filter(period=self.period)

        if self.discipline:
            form = qs.filter(discipline=self.discipline).first()
            if form:
                return form

        return qs.first()

    @cached_property
    def place(self) -> "Place":
        """The place of the internship."""
        return self.project_place.place

    @property
    def program(self) -> Optional["Program"]:
        """The program of the internship."""
        return self.period.program_internship.block.program if self.period else None

    @property
    def total_hours(self) -> tuple[int, int]:
        """The total amount of (hours, minutes) worked during the internship."""
        return sum_times([timesheet.duration for timesheet in self.timesheets.all()])

    @property
    def global_score(self):
        """Global score as defined in the evaluation_form."""
        try:
            evaluation = self.evaluations.filter(intermediate=0).first()
            evaluation_form = self.evaluation_form

            if not evaluation_form:
                return None

            scores = {score["value"]: score for score in evaluation_form.definition["scores"]}
            return scores[evaluation.data["global_score"]]
        except Exception:
            return None

    def accepts_cases(self) -> bool:
        raise NotImplementedError

    def get_available_disciplines(self) -> models.QuerySet:
        """Returns a set of all available disciplines included in the constraints.

        Returns:
            QuerySet: A QuerySet of Discipline objects.
        """
        program_disciplines = self.period.program_internship.get_available_disciplines()

        if program_disciplines.count() > 0:
            return program_disciplines

        return self.track.get_available_disciplines() if self.track else Discipline.objects.none()

    def get_covered_disciplines(self) -> models.QuerySet:
        """If a track exists, it returns a list of disciplines that have already been covered by this student.

        Returns:
            QuerySet: A QuerySet of Discipline objects.
        """
        if self.track is None or self.student is None:
            return Discipline.objects.none()

        skip = {self.CANCELLED, self.UNSUCCESSFUL}
        past_internships = (
            self.student.internships.exclude(pk=self.pk)
            .exclude(status__in=skip)
            .filter(track=self.track, start_date__lt=self.start_date)
        )
        return Discipline.objects.filter(internships__in=past_internships)

    def get_counter_for_disciplines(self) -> Counter:
        """Returns a dictionary of discipline IDs and their count for this internship.

        Returns:
            Dict: A dictionary of disciplines and their count for this internship.
        """
        if not self.track:
            return Counter()

        return Counter(self.get_covered_disciplines().values_list("id", flat=True))


class Mentor(BaseModel):
    """A Mentor is a User that is linked to an Internship."""

    internship = models.ForeignKey(Internship, related_name="mentors", on_delete=models.CASCADE)
    user = models.ForeignKey("metis.User", related_name="mentorships", on_delete=models.PROTECT)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "metis_internship_mentors"
        unique_together = ("internship", "user")

    def clean(self) -> None:
        """TODO: check if there are issues when a contact is removed after the internship has been created.
        Normally we don't need to change this entry anymore, so it should be ok.
        """
        if not self.internship.place.contacts.filter(user_id=self.user_id, is_mentor=True).exists():  # type: ignore
            raise ValidationError("The chosen user is not a valid mentor for the chosen place.")
        return super().clean()
