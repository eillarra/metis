from django.db import models
from django.utils import timezone

from ..base import BaseModel
from .project_places import ProjectPlace


class ImportantDateManager(models.Manager):
    def filter_active(self):
        return self.filter(start_at__lte=timezone.now(), end_at__gte=timezone.now())


class ImportantDate(BaseModel):
    """
    In a Project, important dates help define the steps needed to take during the internship process.
    These dates can be assigned to the whole project or to a Period (and thus to a specific Block).
    """

    PROJECT_PLACE_AVAILABILITY = "project_place_availability"
    PROJECT_PLACE_INFORMATION = "project_place_information"
    STUDENT_INFORMATION = "student_information"
    STUDENT_PREFERENCES = "student_preferences"
    TYPE_CHOICES = (
        (PROJECT_PLACE_AVAILABILITY, "ProjectPlace availability"),
        (PROJECT_PLACE_INFORMATION, "ProjectPlace information"),
        (STUDENT_INFORMATION, "Student information"),
        (STUDENT_PREFERENCES, "Student preferences"),
    )
    TYPES_WITH_FORM = (PROJECT_PLACE_INFORMATION, STUDENT_INFORMATION)

    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    project = models.ForeignKey("metis.Project", related_name="important_dates", on_delete=models.CASCADE)
    period = models.ForeignKey(
        "metis.Period", related_name="important_dates", on_delete=models.CASCADE, null=True, blank=True
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    form = models.ForeignKey(
        "metis.CustomForm", related_name="important_dates", on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = ImportantDateManager()

    class Meta:
        db_table = "metis_project_dates"

    def clean(self) -> None:
        if self.form and self.form.project != self.project:
            raise ValueError("The form must belong to the same project.")
        if not self.form and self.type in self.TYPES_WITH_FORM:
            raise ValueError("This type of date requires a form.")
        return super().clean()

    @property
    def is_active(self) -> bool:
        return self.start_at <= timezone.now() <= self.end_at


def get_project_places_for_date(important_date: ImportantDate) -> models.QuerySet["ProjectPlace"]:
    """
    Returns the places that should be notified for a given important date.
    """

    valid_types = {ImportantDate.PROJECT_PLACE_AVAILABILITY, ImportantDate.PROJECT_PLACE_INFORMATION}

    if important_date.type not in valid_types:
        raise ValueError(f"Invalid type: {important_date.type}")

    if not important_date.period:
        return ProjectPlace.objects.filter(project=important_date.project)

    return ProjectPlace.objects.filter(availability_set__period=important_date.period, availability_set__min__gt=0)
