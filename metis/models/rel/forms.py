from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from metis.services.form_builder import validators as form_validators
from ..base import BaseModel


class CustomForm(BaseModel):
    """
    A custom form.
    """

    PROJECT_PLACE_INFO = "project_place_information"
    STUDENT_INFO = "student_information"
    STUDENT_TOPS = "student_tops"
    CODE_CHOICES = (
        (PROJECT_PLACE_INFO, "Project place information"),
        (STUDENT_INFO, "Student information"),
        (STUDENT_TOPS, "Student tops"),
    )

    project = models.ForeignKey("metis.Project", related_name="forms", on_delete=models.PROTECT)
    code = models.CharField(max_length=32)
    version = models.PositiveSmallIntegerField(default=1)
    definition = models.JSONField(default=dict)

    class Meta:
        db_table = "metis_rel_custom_form"
        unique_together = ("project", "code", "version")

    def clean(self) -> None:
        if self.code == self.STUDENT_TOPS:
            form_validators.validate_tops_form_definition(self.definition)
        else:
            form_validators.validate_custom_form_definition(self.definition)
        return super().clean()

    def save(self, *args, **kwargs) -> None:
        """
        If we already have answers, we don't want to change the definition.
        We should create a new entry with a new version instead.
        """
        if self.pk and self.responses.exists():
            raise ValueError("Cannot change form definition if there are already responses.")
        super().save(*args, **kwargs)

    def clean_data(self, data: dict) -> dict:
        """
        Clean the data for this form.
        """
        if self.code == self.STUDENT_TOPS:
            return form_validators.validate_tops_form_data(self.definition, data, self.project)
        return form_validators.validate_custom_form_data(self.definition, data)


class CustomFormResponse(BaseModel):
    """
    A form entry.
    These can be linked to different models, and can be used to store any kind of data.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="custom_form_responses")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    form = models.ForeignKey(CustomForm, on_delete=models.PROTECT, related_name="responses")
    data = models.JSONField(default=dict)

    class Meta:
        db_table = "metis_rel_custom_form_response"
        unique_together = ("content_type", "object_id", "form")

    def clean(self) -> None:
        self.data = self.form.clean_data(self.data)
        return super().clean()


class CustomFormResponsesMixin(models.Model):
    form_responses = GenericRelation(CustomFormResponse)

    class Meta:
        abstract = True
