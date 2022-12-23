from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Remark(models.Model):
    """
    Remarks made by administrators.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="remarks")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    text = models.TextField()

    created_by = models.ForeignKey("sparta.User", related_name="remarks", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sparta_rel_remark"


class RemarksMixin(models.Model):
    remarks = GenericRelation(Remark)

    class Meta:
        abstract = True
