from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db import models


class Remark(models.Model):
    """
    Remarks made by administrators.
    A copy of the object is saved here for historical purposes.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="remarks")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    text = models.TextField()
    snapshot = models.JSONField(null=True, editable=False)

    created_by = models.ForeignKey("sparta.User", related_name="remarks", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sparta_rel_remark"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.snapshot = serializers.serialize("json", [self.content_object])
        super().save(*args, **kwargs)


class RemarksMixin(models.Model):
    remarks = GenericRelation(Remark)

    class Meta:
        abstract = True
