from django.db import models
from django.utils import timezone

from ..base import BaseModel


class ImportantDate(BaseModel):
    """
    In a Project, important dates help define the steps needed to take during the internship process.
    These dates can be assigned to the whole project or to a Period (and thus to a specific Block).
    """

    TYPE_CHOICES = (
        ("student_information", "Student information"),
        ("student_preferences", "Student preferences"),
        ("project_place_availability", "ProjectPlace availability"),
        ("project_place_information", "ProjectPlace information"),
    )
    TYPES_WITH_FORM = ("student_information", "place_information")

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

    class Meta:
        db_table = "metis_project_dates"

    def clean(self) -> None:
        if self.form and self.form.education != self.project.education:
            raise ValueError("The form must belong to the same education as the project.")
        if not self.form and self.type in self.TYPES_WITH_FORM:
            raise ValueError("This type of date requires a form.")
        return super().clean()

    @property
    def is_active(self) -> bool:
        return self.start_at <= timezone.now() <= self.end_at
