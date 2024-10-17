from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from metis.services.form_builder.custom_forms import validate_form_definition, validate_form_response
from metis.services.form_builder.tops import validate_tops_form_definition, validate_tops_form_response

from ..base import BaseModel
from ..rel.remarks import RemarksMixin
from .internships import Internship
from .project_places import ProjectPlace
from .students import Student


class QuestioningManager(models.Manager):
    def filter_active(self):
        return self.filter(start_at__lte=timezone.now(), end_at__gte=timezone.now())


class Questioning(RemarksMixin, BaseModel):
    """In a Project, questionings define the moments when students / places have to fill in a form.

    The questioning can be assigned to the whole project or to a Period (and thus to a specific Block).
    """

    PROJECT_PLACE_AVAILABILITY = "project_place_availability"
    PROJECT_PLACE_INFORMATION = "project_place_information"
    STUDENT_INFORMATION = "student_information"
    STUDENT_TOPS = "student_tops"
    TYPE_CHOICES = (
        (PROJECT_PLACE_AVAILABILITY, "ProjectPlace availability"),
        (PROJECT_PLACE_INFORMATION, "ProjectPlace information"),
        (STUDENT_INFORMATION, "Student information"),
        (STUDENT_TOPS, "Student preferences"),
    )
    TYPES_WITH_FORM = (PROJECT_PLACE_INFORMATION, STUDENT_INFORMATION)

    # TODO: combine type with target_group
    TARGET_GROUP_CHOICES = (
        ("project_places", "Project Places"),
        ("students", "Students"),
        ("project_places_with_internship", "Project Places with Internship"),
        ("students_with_internship", "Students with Internship"),
    )

    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    target_group = models.CharField(max_length=32, choices=TARGET_GROUP_CHOICES, default="project_places")
    project = models.ForeignKey("metis.Project", related_name="questionings", on_delete=models.CASCADE)
    period = models.ForeignKey(
        "metis.Period", related_name="questionings", on_delete=models.CASCADE, null=True, blank=True
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    form_definition = models.JSONField(default=dict)
    email_subject = models.CharField(max_length=255, default="", blank=True)
    email_body = models.TextField(default="", blank=True)
    email_add_office_in_bcc = models.BooleanField(default=False)
    disable_automatic_emails = models.BooleanField(default=False)

    objects = QuestioningManager()

    class Meta:  # noqa: D106
        db_table = "metis_project_questionings"

    def clean(self) -> None:
        """Validate the data."""
        if self.period and self.period.project != self.project:
            raise ValidationError("The period must belong to the same project.")
        if not self.form_definition and self.type in self.TYPES_WITH_FORM:
            raise ValidationError("This type of questioning requires a custom form definition.")
        if self.form_definition:
            try:
                if self.type == self.STUDENT_TOPS:
                    validate_tops_form_definition(self.form_definition)
                else:
                    validate_form_definition(self.form_definition)
            except ValueError as exc:
                raise ValidationError({"form_definition": str(exc)}) from exc
        return super().clean()

    def clean_response_data(self, data: dict) -> dict:
        """Validate a response for this evaluation form."""
        if self.type == self.STUDENT_TOPS:
            return validate_tops_form_response(self.form_definition, data, self.project)
        return validate_form_response(self.form_definition, data)

    @property
    def title(self) -> str:
        """Returns the title of this questioning."""
        try:
            return self.form_definition["title"]["nl"]
        except (KeyError, TypeError):
            return self.type.replace("_", " ").capitalize()

    @property
    def file_url(self) -> str:
        return reverse("questioning_file", kwargs={"questioning_id": self.id, "file_type": "pdf"})

    @property
    def has_email(self) -> bool:
        """A boolean indicating whether this questioning has an email."""
        return bool(self.email_subject and self.email_body)

    @property
    def is_active(self) -> bool:
        """A boolean indicating whether this questioning is active."""
        return self.start_at <= timezone.now() <= self.end_at

    @property
    def random_seed(self) -> int | None:
        """The random seed for this questioning, that can be used by a planner."""
        try:
            return int(self.responses.order_by("created_at").first().created_at.timestamp())
        except AttributeError:
            return None

    @property
    def response_rate(self) -> float:
        """The response rate for this questioning."""
        try:
            return self.responses.count() / self.get_target_group_size()  # type: ignore
        except ZeroDivisionError:
            return 0.0

    def get_support_data(self) -> dict:
        """Return the support data for this questioning."""
        if self.type == self.STUDENT_TOPS:
            return {"project_places": self.project.project_places.select_related("place").all()}
        return {}

    def get_target_group(self) -> models.QuerySet["ProjectPlace"] | models.QuerySet["Student"]:
        """Return the target group for this questioning."""
        queryset = models.QuerySet()

        if self.target_group in {"project_places", "project_places_with_internship"}:
            queryset = get_project_places_for_questioning(self).distinct()

        if self.target_group in {"students", "students_with_internship"}:
            queryset = get_students_for_questioning(self).distinct()

        if self.target_group in {"project_places_with_internship", "students_with_internship"}:
            return queryset.filter(
                internships__project=self.project,
                internships__period=self.period,
                internships__status=Internship.DEFINITIVE,
            )

        return queryset

    def get_target_group_size(self) -> int:
        """Return the size of the target group for this questioning."""
        return self.get_target_group().count()


def get_project_places_for_questioning(questioning: Questioning) -> models.QuerySet["ProjectPlace"]:
    """Return the places that should be notified for a given questioning."""
    valid_types = {Questioning.PROJECT_PLACE_AVAILABILITY, Questioning.PROJECT_PLACE_INFORMATION}

    if questioning.type not in valid_types:
        raise ValueError(f"Invalid type: {questioning.type}")

    if questioning.period:
        return questioning.period.project_places

    return questioning.project.project_places


def get_students_for_questioning(questioning: Questioning) -> models.QuerySet["Student"]:
    """Return the students that should be notified for a given questioning."""
    valid_types = {Questioning.STUDENT_INFORMATION, Questioning.STUDENT_TOPS}

    if questioning.type not in valid_types:
        raise ValueError(f"Invalid type: {questioning.type}")

    if questioning.period:
        return questioning.period.students

    return questioning.project.students
