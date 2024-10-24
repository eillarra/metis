import math
from collections import Counter
from datetime import date, datetime, time, timedelta
from hashlib import sha1
from math import ceil
from typing import TYPE_CHECKING, NamedTuple, Optional
from uuid import uuid4

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from metis.utils.dates import sum_times

from ..base import BaseModel, TagsMixin
from ..disciplines import Discipline
from ..rel.files import FilesMixin, append_files_tags
from ..rel.remarks import RemarksMixin, append_remarks_tags
from .evaluations import EvaluationForm


if TYPE_CHECKING:
    from ..educations import Education
    from ..places import Place
    from ..rel.signatures import Signature
    from .programs import Program


class EvaluationPeriod(NamedTuple):
    """A named tuple for an evaluation period."""

    intermediate: int
    start_at: datetime
    end_at: datetime
    official_deadline: date

    def is_final(self) -> bool:
        """Check if the evaluation period is the final one."""
        return self.intermediate == 0


def get_cached_evaluation_form(
    project_id: int, period_id: int | None = None, discipline_id: int | None = None
) -> Optional["EvaluationForm"]:
    """Get the evaluation form for a period and discipline.

    This checks a cache of evaluation forms for the project, period and discipline to reduce database queries.
    Necessary when requesting long lists of internships with the evaluation periods for the new UI.

    :param project_id: The ID of the project.
    :param period_id: The ID of the period.
    :param discipline_id: The ID of the discipline.
    :returns: The evaluation form for the period and discipline.
    """
    cache_key = f"evaluation_form_{project_id}_{period_id}_{discipline_id}"
    evaluation_form = cache.get(cache_key)

    if evaluation_form:
        return evaluation_form if evaluation_form != "EvaluationForm.NotFound" else None

    qs = EvaluationForm.objects.filter(project_id=project_id)

    if period_id and qs.filter(period_id=period_id).exists():
        qs = qs.filter(period_id=period_id)

    if discipline_id and qs.filter(discipline_id=discipline_id).exists():
        qs = qs.filter(discipline_id=discipline_id)

    evaluation_form = qs.first()
    cache.set(cache_key, evaluation_form or "EvaluationForm.NotFound", 5)

    return evaluation_form


def get_evaluation_periods(start_date: date, end_date: date, intermediates: int = 0) -> list[EvaluationPeriod]:
    """Get the evaluation periods based on the start and end date of the internship and a number of intermediates.

    If there are no intermediates, only a final evaluation is returned.
    Evaluation periods are calculated as follows:
    - first evaluation: starts at the start of the internship, ends a day before next one (if exists) starts
    - intermediate evaluations: start a day after the previous one ends, ends a day before next one starts
    - final evaluation: starts a day after the last intermediate ends, ends a month after the end of the internship

    :param start_date: The start date of the internship.
    :param end_date: The end date of the internship.
    :param intermediates: The number of intermediate evaluations.
    :returns: A list of EvaluationPeriod tuples with the start and end date of the evaluation periods.
    """
    full_duration = (end_date - start_date).days
    evaluation_periods = []
    grace_period = 14 if full_duration > 60 and intermediates < 2 else 7

    # for each evaluation, get the start and end date
    if intermediates > 0:
        evaluation_block = (end_date - start_date).days // (intermediates + 1)
        evaluation_deadlines = [start_date + timedelta(days=(evaluation_block * i)) for i in range(intermediates + 1)]
        evaluation_dates = [
            start_date + timedelta(days=(evaluation_block * i) + grace_period) for i in range(intermediates + 1)
        ]

        for i in range(intermediates):
            start_at = timezone.make_aware(
                datetime.combine(evaluation_deadlines[i], time(6, 0)),
                timezone.get_current_timezone(),
            )
            end_at = timezone.make_aware(
                datetime.combine(evaluation_dates[i + 1] - timedelta(days=1), time(23, 59)),
                timezone.get_current_timezone(),
            )

            evaluation_periods.append(
                EvaluationPeriod(
                    intermediate=i + 1,
                    start_at=start_at,
                    end_at=end_at,
                    official_deadline=evaluation_deadlines[i + 1],
                )
            )

    # add the final evaluation
    final_start = (
        evaluation_periods[-1][2] + timedelta(days=1)
        if intermediates > 0
        else start_date + timedelta(days=grace_period)
    )
    final_end = end_date + timedelta(days=grace_period)

    final_at = timezone.make_aware(
        datetime.combine(final_start, time(6, 0)),
        timezone.get_current_timezone(),
    )
    end_at = timezone.make_aware(
        datetime.combine(final_end, time(23, 59)),
        timezone.get_current_timezone(),
    )

    evaluation_periods.append(
        EvaluationPeriod(
            intermediate=0,
            start_at=final_at,
            end_at=end_at,
            official_deadline=end_date,
        )
    )

    return evaluation_periods


def get_internship_tags(obj: "Internship", *, type: str = "all") -> list[str]:
    """For an internship, process the tags.

    :param obj: An instance of the Internship class.
    :param type: The type of tags to process.
    :returns: A list of tags.
    """
    tags = obj.tags

    # evaluations
    if type in {"all", "evaluations"} and obj.pk and obj.evaluation_form:
        tags = [tag for tag in tags if not tag.startswith("intermediate.")]
        evaluations = obj.evaluations.all()

        for i in range(0, obj.evaluation_form.definition["intermediate_evaluations"] + 1):
            if evaluations.filter(intermediate=i, is_self_evaluation=False, is_approved=True).exists():
                tags.append(f"intermediate.{i}:approved")
            elif evaluations.filter(intermediate=i, is_self_evaluation=False, is_approved=False).exists():
                tags.append(f"intermediate.{i}:not_approved")
            else:
                tags.append(f"intermediate.{i}:pending")

            if obj.evaluation_form.has_self_evaluations:
                if evaluations.filter(intermediate=i, is_self_evaluation=True, is_approved=True).exists():
                    tags.append(f"intermediate.{i}.self:approved")
                elif evaluations.filter(intermediate=i, is_self_evaluation=True, is_approved=False).exists():
                    tags.append(f"intermediate.{i}.self:not_approved")
                else:
                    tags.append(f"intermediate.{i}.self:pending")

    # hours
    if type in {"all", "hours"}:
        tags = [tag for tag in tags if not tag.startswith("hours.")]
        hours, minutes = obj.total_hours
        accepted_hours, accepted_minutes = obj.get_total_hours(approved_only=True)
        tags.append(f'hours.total:"{hours}:{minutes:02d}"')
        tags.append(f'hours.approved:"{accepted_hours}:{accepted_minutes:02d}"')

    # files
    if type in {"all", "files"}:
        tags = append_files_tags(obj, tags=tags)

    # remarks
    if type in {"all", "remarks"}:
        tags = append_remarks_tags(obj, tags=tags)

    return list(set(tags))


def get_remaining_discipline_constraints(obj: "Internship") -> list[dict]:
    """Calculate the remaining discipline constraints based on the track constraints.

    :param obj: An instance of the Internship class.
    :returns: A list of remaining DisciplineConstraint objects.
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

    :param obj: An instance of the Internship class.
    :raises ValidationError: If the chosen discipline is not available for the internship program
        or does not meet the remaining constraints for the student.
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


class Internship(FilesMixin, RemarksMixin, TagsMixin, BaseModel):
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
    def update_tags(cls, internship: "Internship", *, type: str = "all") -> None:
        """Update tags for an internship, without calling clean() on the model."""
        tags = get_internship_tags(internship, type=type)
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
        """The evaluation form for this internship."""
        return get_cached_evaluation_form(self.project_id, self.period_id, self.discipline_id)  # type: ignore

    @property
    def evaluation_periods(self) -> list[EvaluationPeriod]:
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
        return self.get_total_hours()

    @property
    def final_score(self) -> float | None:
        """The final score for the internship."""
        from metis.services.evaluator import get_evaluator

        return get_evaluator(self).evaluate()

    @property
    def secret(self) -> str:
        """A secret string for the internship."""
        return sha1(f"{self.uuid}{settings.SECRET_KEY}".encode()).hexdigest()

    def accepts_cases(self) -> bool:
        """Check if the internship accepts cases."""
        raise NotImplementedError

    def get_available_disciplines(self) -> models.QuerySet:
        """Return a set of all available disciplines included in the constraints.

        :returns: A QuerySet of Discipline objects.
        """
        program_disciplines = self.period.program_internship.get_available_disciplines()

        if program_disciplines.count() > 0:
            return program_disciplines

        return self.track.get_available_disciplines() if self.track else Discipline.objects.none()

    def get_covered_disciplines(self) -> models.QuerySet:
        """If a track exists, it returns a list of disciplines that have already been covered by this student.

        :returns: A QuerySet of Discipline objects.
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

        :returns: A dictionary of disciplines and their count for this internship.
        """
        if not self.track:
            return Counter()

        return Counter(self.get_covered_disciplines().values_list("id", flat=True))

    def get_evaluation_periods(self, evaluation_form: "EvaluationForm") -> list[EvaluationPeriod]:
        """Get the evaluation periods for the internship."""
        return get_evaluation_periods(
            self.start_date, self.end_date, evaluation_form.definition["intermediate_evaluations"]
        )

    def get_total_hours(self, *, approved_only: bool = False) -> tuple[int, int]:
        """Get the total amount of (hours, minutes) worked during the internship."""
        if approved_only:
            return sum_times([timesheet.duration for timesheet in self.timesheets.filter(is_approved=True)])
        return sum_times([timesheet.duration for timesheet in self.timesheets.all()])

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

    internship = models.ForeignKey("metis.Internship", related_name="mentors", on_delete=models.CASCADE)
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
