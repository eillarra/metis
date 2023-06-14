from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from metis.services.form_builder import validate_form_definition, validate_form_data
from ..base import BaseModel


class CustomForm(BaseModel):
    """
    A custom form.
    """

    PROJECT_PLACE_INFO = "project_place_information"
    STUDENT_INFO = "student_information"
    CODE_CHOICES = (
        (PROJECT_PLACE_INFO, "Project place information"),
        (STUDENT_INFO, "Student information"),
    )

    education = models.ForeignKey("metis.Education", related_name="forms", on_delete=models.PROTECT)
    code = models.CharField(max_length=32)
    version = models.PositiveSmallIntegerField(default=1)
    definition = models.JSONField(default=dict)

    class Meta:
        db_table = "metis_rel_custom_form"
        unique_together = ("education", "code", "version")

    def clean(self) -> None:
        validate_form_definition(self.definition)
        return super().clean()

    def save(self, *args, **kwargs) -> None:
        """
        If we already have answers, we don't want to change the definition.
        We should create a new entry with a new version instead.
        """
        if self.pk and self.entries.exists():
            raise ValueError("Cannot change form definition if there are already entries.")
        super().save(*args, **kwargs)


class CustomFormResponse(BaseModel):
    """
    A form entry.
    These can be linked to different models, and can be used to store any kind of data.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="custom_form_responses")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    form = models.ForeignKey(CustomForm, on_delete=models.PROTECT, related_name="entries")
    data = models.JSONField(default=dict)

    class Meta:
        db_table = "metis_rel_custom_form_response"
        unique_together = ("content_type", "object_id", "form")

    def clean(self) -> None:
        validate_form_data(self.form.definition, self.data)
        return super().clean()


class CustomFormResponsesMixin(models.Model):
    form_responses = GenericRelation(CustomFormResponse)

    class Meta:
        abstract = True
