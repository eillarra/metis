from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..base import BaseModel
from .snapshots import save_snapshot


class Remark(BaseModel):
    """
    Remarks made by administrators.
    A copy of the object is saved here for historical purposes.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="remarks")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    text = models.TextField()

    class Meta:
        db_table = "metis_rel_remark"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        save_snapshot(self.content_object.__class__, self.content_object, user=self.created_by)  # type: ignore


class RemarksMixin(models.Model):
    remarks = GenericRelation(Remark)

    class Meta:
        abstract = True
