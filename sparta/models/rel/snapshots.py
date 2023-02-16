from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.db import models


class Snapshot(models.Model):
    """
    A copy of the object is saved here for historical purposes.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="snapshots")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    data = models.JSONField(null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sparta_rel_snapshot"


class SnapshotsMixin(models.Model):
    snapshots = GenericRelation(Snapshot)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        save_snapshot(self.__class__, self)


def save_snapshot(sender, instance, **kwargs):
    if sender == Snapshot:
        return

    serialized_data = serialize("json", [instance])

    snapshot = Snapshot()
    snapshot.content_object = instance
    snapshot.data = serialized_data
    snapshot.save()
