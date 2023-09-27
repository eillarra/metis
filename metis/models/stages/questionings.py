from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from metis.services.form_builder import validators as form_validators
from ..base import BaseModel
from .project_places import ProjectPlace
from .students import Student


class QuestioningManager(models.Manager):
    def filter_active(self):
        return self.filter(start_at__lte=timezone.now(), end_at__gte=timezone.now())


class Questioning(BaseModel):
    """
    In a Project, questionings define the moments when students / places have to fill in a form.
    The dates can be assigned to the whole project or to a Period (and thus to a specific Block).
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

    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    project = models.ForeignKey("metis.Project", related_name="questionings", on_delete=models.CASCADE)
    period = models.ForeignKey(
        "metis.Period", related_name="questionings", on_delete=models.CASCADE, null=True, blank=True
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    form_definition = models.JSONField(default=dict)

    objects = QuestioningManager()

    class Meta:
        db_table = "metis_project_questionings"

    def clean(self) -> None:
        if self.period and self.period.project != self.project:
            raise ValidationError("The period must belong to the same project.")
        if not self.form_definition and self.type in self.TYPES_WITH_FORM:
            raise ValidationError("This type of questioning requires a custom form definition.")
        if self.form_definition:
            try:
                if self.type == self.STUDENT_TOPS:
                    form_validators.validate_tops_form_definition(self.form_definition)
                else:
                    form_validators.validate_form_definition(self.form_definition)
            except ValueError as e:
                raise ValidationError({"form_definition": str(e)})
        return super().clean()

    def clean_response_data(self, data: dict) -> dict:
        """
        Clean the response for this form.
        """
        if self.type == self.STUDENT_TOPS:
            return form_validators.validate_tops_form_response(self.form_definition, data, self.project)
        return form_validators.validate_form_response(self.form_definition, data)

    @property
    def is_active(self) -> bool:
        return self.start_at <= timezone.now() <= self.end_at

    @property
    def response_rate(self) -> float:
        return self.responses.count() / self.get_target_group_size()  # type: ignore

    def get_target_group(self) -> models.QuerySet["ProjectPlace"] | models.QuerySet["Student"]:
        if self.type in {self.PROJECT_PLACE_AVAILABILITY, self.PROJECT_PLACE_INFORMATION}:
            return get_project_places_for_questioning(self)
        if self.type in {self.STUDENT_INFORMATION, self.STUDENT_TOPS}:
            return get_students_for_questioning(self)
        raise ValueError(f"Invalid type: {self.type}")

    def get_target_group_size(self) -> int:
        return self.get_target_group().count()


def get_project_places_for_questioning(questioning: Questioning) -> models.QuerySet["ProjectPlace"]:
    """
    Returns the places that should be notified for a given questioning.
    """

    valid_types = {Questioning.PROJECT_PLACE_AVAILABILITY, Questioning.PROJECT_PLACE_INFORMATION}

    if questioning.type not in valid_types:
        raise ValueError(f"Invalid type: {questioning.type}")

    if questioning.period:
        return questioning.period.project_places

    return questioning.project.project_places


def get_students_for_questioning(questioning: Questioning) -> models.QuerySet["Student"]:
    """
    Returns the students that should be notified for a given questioning.
    """

    valid_types = {Questioning.STUDENT_INFORMATION, Questioning.STUDENT_TOPS}

    if questioning.type not in valid_types:
        raise ValueError(f"Invalid type: {questioning.type}")

    if questioning.period:
        return questioning.period.students

    return questioning.project.students
