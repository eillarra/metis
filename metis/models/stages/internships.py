import math
from collections import Counter
from datetime import date, datetime, time, timedelta
from hashlib import sha1
from math import ceil
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from metis.utils.dates import sum_times

from ..base import BaseModel
from ..disciplines import Discipline
from ..rel.remarks import RemarksMixin


if TYPE_CHECKING:
    from ..educations import Education
    from ..places import Place
    from ..rel.signatures import Signature
    from .evaluations import EvaluationForm
    from .programs import Program


def get_evaluation_periods(
    start_date: date, end_date: date, intermediates: int = 0
) -> list[tuple[int, datetime, datetime]]:
    """Get the evaluation periods based on the start and end date of the internship and a number of intermediates.

    If there are no intermediates, only a final evaluation is returned.
    Evaluation periods are calculated as a week, approximately 4 days before and 3 days after the end of the internship.

    :param start_date: The start date of the internship.
    :param end_date: The end date of the internship.
    :param intermediates: The number of intermediate evaluations.
    :return: A list of tuples with the start and end date of the evaluation periods.
    """
    evaluation_periods = []

    if intermediates > 0:
        duration = (end_date - start_date).days
        days_before, days_after = 4, 4
        evaluation_block = duration // (intermediates + 1)

        for i in range(intermediates):
            intermediate = start_date + timedelta(days=evaluation_block * (i + 1))
            start = timezone.make_aware(
                datetime.combine(intermediate - timedelta(days=days_before), time(6, 0)),
                timezone.get_current_timezone(),
            )
            end = timezone.make_aware(
                datetime.combine(intermediate + timedelta(days=days_after), time(23, 59)),
                timezone.get_current_timezone(),
            )
            evaluation_periods.append((i + 1, start, end))

    final_start = timezone.make_aware(
        datetime.combine(end_date - timedelta(days=days_before), time(6, 0)), timezone.get_current_timezone()
    )
    final_end = timezone.make_aware(
        datetime.combine(end_date + timedelta(days=days_after), time(23, 59)), timezone.get_current_timezone()
    )
    evaluation_periods.append((0, final_start, final_end))

    return evaluation_periods


def get_internship_tags(obj: "Internship") -> list[str]:
    """For an internship, process the tags.

    :param obj: An instance of the Internship class.
    :return: A list of tags.
    """
    tags = []
    tags = [tag for tag in obj.tags if not tag.startswith("intermediate.")]

    # evaluation tags
    if obj.pk and obj.evaluation_form:
        intermediates = obj.evaluation_form.definition["intermediate_evaluations"]
        evaluations = obj.evaluations.all()

        for i in range(0, intermediates + 1):
            if evaluations.filter(intermediate=i, is_approved=True).exists():
                tags.append(f"intermediate.{i}:approved")
            elif evaluations.filter(intermediate=i, is_approved=False).exists():
                tags.append(f"intermediate.{i}:not_approved")
            else:
                tags.append(f"intermediate.{i}:pending")

    return list(set(tags))


def get_remaining_discipline_constraints(obj: "Internship") -> list[dict]:
    """Calculate the remaining discipline constraints based on the track constraints.

    :param obj: An instance of the Internship class.
    :return: A list of remaining DisciplineConstraint objects.
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
    project_place = models.ForeignKey(
        "metis.ProjectPlace", related_name="internships", null=True, on_delete=models.PROTECT
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)

    discipline = models.ForeignKey("metis.Discipline", related_name="internships", null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CONCEPT)

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    tags = models.JSONField(default=list)

    # evaluation_deadline = models.DateField()  # this can be used for cases > reviews
    # reviewers (beoordelaars)

    def clean(self) -> None:
        """Validate the internship data.

        Things to check:
        - only if status is `preplanning`, the place can be None  # TODO
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
        if not self.project_place and self.status != self.PREPLANNING:
            raise ValidationError("A place is required if the internship is not in preplanning status.")

        validate_discipline_choice(self)
        return super().clean()

    def save(self, *args, **kwargs) -> None:
        """Save the internship.

        Some fields are automatically filled in when the internship is created:
        - start_date and end_date are filled in based on the period (if not already set)
        - is_approved is set to True if the education has automatic_internship_approval enabled
        """
        if not self.pk and self.period:
            if not self.start_date:
                self.start_date = self.period.start_date
            if not self.end_date:
                self.end_date = self.period.end_date

        if (
            not self.pk
            and self.project.education.configuration
            and self.project.education.configuration["automatic_internship_approval"]
        ):
            self.is_approved = self.status != self.PREPLANNING

        self.tags = get_internship_tags(self)

        super().save(*args, **kwargs)

    @classmethod
    def approve(cls, internship: "Internship", signature: "Signature") -> None:
        """Approve an internship, without calling clean() on the model. A signature is required.

        This is done by the Place admin.
        """
        if not signature or not signature.content_object == internship:
            raise ValidationError("A signature is required to approve an internship.")

        if not internship.is_approved:
            cls.objects.filter(id=internship.id).update(is_approved=True)  # type: ignore

    @classmethod
    def update_tags(cls, internship: "Internship") -> None:
        """Update tags for an internship, without calling clean() on the model."""
        tags = get_internship_tags(internship)
        cls.objects.filter(id=internship.id).update(tags=tags)

    def can_be_managed_by(self, user) -> bool:
        """Check if the user can manage this internship."""
        return self.project.can_be_managed_by(user)

    def can_be_viewed_by(self, user) -> bool:
        """Check if the user can view this internship."""
        return (
            self.student.user == user
            or self.mentors.filter(user=user).exists()
            or (self.place.can_be_managed_by(user) if self.place else False)
        )

    @property
    def is_active(self) -> bool:
        """A boolean indicating whether the internship is active or not."""
        return self.start_date <= timezone.now().date() <= self.end_date

    @property
    def block_name(self) -> str:
        """The name of the block of the internship."""
        return self.period.program_internship.block.name if self.period else ""

    @property
    def duration_weeks(self) -> int:
        """The duration of the internship in weeks."""
        return ceil((self.end_date - self.start_date).days / 7)

    @property
    def education(self) -> "Education":
        """The education of the internship."""
        return self.project.education

    @property
    def evaluation_form(self) -> Optional["EvaluationForm"]:
        """The evaluation form for this internship."""  # noqa: D401
        qs = self.project.evaluation_forms.all()

        if self.period and qs.filter(period=self.period).exists():
            qs = self.period.evaluation_forms.filter(period=self.period)

        if self.discipline:
            form = qs.filter(discipline=self.discipline).first()
            if form:
                return form

        return qs.first()

    @property
    def evaluation_periods(self) -> list[tuple[int, datetime, datetime]]:
        """The evaluation periods for the internship."""
        if not self.evaluation_form:
            return []

        return self.get_evaluation_periods(self.evaluation_form)

    @property
    def place(self) -> Optional["Place"]:
        """The place of the internship."""
        return self.project_place.place if self.project_place else None

    @property
    def program(self) -> Optional["Program"]:
        """The program of the internship."""
        return self.period.program_internship.block.program if self.period else None

    @property
    def total_hours(self) -> tuple[int, int]:
        """The total amount of (hours, minutes) worked during the internship."""
        return sum_times([timesheet.duration for timesheet in self.timesheets.all()])

    @property
    def global_score(self) -> dict | None:
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

    @property
    def secret(self) -> str:
        """A secret string for the internship."""
        return sha1(f"{self.uuid}{settings.SECRET_KEY}".encode()).hexdigest()

    def accepts_cases(self) -> bool:
        """Check if the internship accepts cases."""
        raise NotImplementedError

    def get_available_disciplines(self) -> models.QuerySet:
        """Return a set of all available disciplines included in the constraints.

        :return: A QuerySet of Discipline objects.
        """
        program_disciplines = self.period.program_internship.get_available_disciplines()

        if program_disciplines.count() > 0:
            return program_disciplines

        return self.track.get_available_disciplines() if self.track else Discipline.objects.none()

    def get_covered_disciplines(self) -> models.QuerySet:
        """If a track exists, it returns a list of disciplines that have already been covered by this student.

        :return: A QuerySet of Discipline objects.
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
        """Return a dictionary of discipline IDs and their count for this internship.

        :return: A dictionary of disciplines and their count for this internship.
        """
        if not self.track:
            return Counter()

        return Counter(self.get_covered_disciplines().values_list("id", flat=True))

    def get_evaluation_periods(self, evaluation_form: "EvaluationForm") -> list[tuple[int, datetime, datetime]]:
        """Get the evaluation periods for the internship."""
        return get_evaluation_periods(
            self.start_date, self.end_date, evaluation_form.definition["intermediate_evaluations"]
        )

    def get_secret_generated_file_url(self, template_code: str) -> str:
        """Get the secret URL for the internship."""
        return reverse("internship_pdf_secret", args=[self.uuid, self.secret, template_code])

    def get_secret_file_url(self, file_code: str) -> str:
        """Get the secret URL for the stagegids. We need an extra method so it can be used in email templates."""
        file = self.project.files.filter(code=file_code).first()
        return reverse("internship_media_file_secret", args=[self.uuid, self.secret, file.file]) if file else "#"

    def __getattr__(self, name: str) -> str:
        """Handle dynamic method calls for secret URLs."""
        if name.startswith("get_secret_url_"):
            template_code = name[len("get_secret_url_") :]
            return self.get_secret_generated_file_url(template_code)
        if name.startswith("get_secret_file_url_"):
            file_code = name[len("get_secret_file_url_") :]
            file_code = file_code.replace("__", ":")
            return self.get_secret_file_url(file_code)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class Mentor(BaseModel):
    """A Mentor is a User that is linked to an Internship."""

    internship = models.ForeignKey(Internship, related_name="mentors", on_delete=models.CASCADE)
    user = models.ForeignKey("metis.User", related_name="mentorships", on_delete=models.PROTECT)
    is_primary = models.BooleanField(default=False)

    class Meta:  # noqa: D106
        db_table = "metis_internship_mentors"
        unique_together = ("internship", "user")

    def clean(self) -> None:
        """TODO: check if there are issues when a contact is removed after the internship has been created.
        Normally we don't need to change this entry anymore, so it should be ok.
        """
        if not self.internship.place.contacts.filter(user_id=self.user_id, is_mentor=True).exists():  # type: ignore
            raise ValidationError("The chosen user is not a valid mentor for the chosen place.")
        return super().clean()
