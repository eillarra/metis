from django.core.exceptions import ValidationError
from django.db import models

from metis.models.base import BaseModel
from metis.services.form_builder import validators as form_validators


class EvaluationForm(BaseModel):
    project = models.ForeignKey("metis.Project", related_name="evaluation_forms", on_delete=models.CASCADE)
    period = models.ForeignKey(
        "metis.Period", related_name="evaluation_forms", on_delete=models.CASCADE, null=True, blank=True
    )
    discipline = models.ForeignKey(
        "metis.Discipline", related_name="evaluation_forms", on_delete=models.CASCADE, null=True, blank=True
    )

    form_definition = models.JSONField(default=dict)
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()
    email_add_office_in_bcc = models.BooleanField(default=False)
    version = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = "metis_project_evaluation_forms"
        unique_together = ("project", "period", "discipline", "version")
        ordering = ["project", "-version"]

    def clean(self) -> None:
        try:
            form_validators.validate_evaluation_form_definition(self.form_definition)
        except ValueError as exc:
            raise ValidationError({"form_definition": str(exc)}) from exc
        return super().clean()

    def clean_response_data(self, data: dict) -> dict:
        """
        Clean the response for this evaluation form.
        """
        return form_validators.validate_evaluation_form_response(self.form_definition, data)

    @property
    def definition(self) -> dict:
        return form_validators.EvaluationForm(**self.form_definition).model_dump()
