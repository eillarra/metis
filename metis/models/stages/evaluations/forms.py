from django.core.exceptions import ValidationError
from django.db import models

from metis.models.base import BaseModel
from metis.services.form_builder.evaluations import (
    validate_evaluation_form_definition,
    validate_evaluation_form_response,
)


class EvaluationForm(BaseModel):
    """A form that can be used to evaluate an Internship."""

    project = models.ForeignKey("metis.Project", related_name="evaluation_forms", on_delete=models.CASCADE)
    period = models.ForeignKey(
        "metis.Period", related_name="evaluation_forms", on_delete=models.CASCADE, null=True, blank=True
    )
    discipline = models.ForeignKey(
        "metis.Discipline", related_name="evaluation_forms", on_delete=models.CASCADE, null=True, blank=True
    )

    form_definition = models.JSONField(default=dict)
    version = models.PositiveSmallIntegerField(default=1)
    has_self_evaluations = models.BooleanField(default=False)

    class Meta:  # noqa: D106
        db_table = "metis_project_evaluation_forms"
        unique_together = ("project", "period", "discipline", "version")
        ordering = ["project", "-version"]

    def clean(self) -> None:
        """Validate the form definition."""
        try:
            validate_evaluation_form_definition(self.form_definition)
        except ValueError as exc:
            raise ValidationError({"form_definition": str(exc)}) from exc
        return super().clean()

    def clean_response_data(self, data: dict) -> dict:
        """Validate a response for this evaluation form."""
        return validate_evaluation_form_response(self.form_definition, data)

    @property
    def definition(self) -> dict:
        """Return the form definition with default values filled in."""
        return validate_evaluation_form_definition(self.form_definition).model_dump()
