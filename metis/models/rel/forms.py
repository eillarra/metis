from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..base import BaseModel


class FormResponse(BaseModel):
    """
    A form entry.
    These can be linked to different models, and can be used to store any kind of data.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="custom_form_responses")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    questioning = models.ForeignKey("metis.Questioning", on_delete=models.PROTECT, related_name="responses")
    data = models.JSONField(default=dict)

    class Meta:
        db_table = "metis_rel_form_response"
        unique_together = ("content_type", "object_id", "questioning")

    def clean(self) -> None:
        self.data = self.questioning.clean_response_data(self.data)
        return super().clean()


class FormResponsesMixin(models.Model):
    form_responses = GenericRelation(FormResponse)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        # TODO: pre_delete makes more sense, but it has to be set for each model
        if self.form_responses.exists():
            raise models.ProtectedError("Cannot delete object with form responses.", self.form_responses.all())
        return super().delete(using, keep_parents)
