from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..base import BaseModel
from .snapshots import save_snapshot


class Remark(BaseModel):
    """Remarks made by administrators.

    Every time a remark is made, a copy of the object is saved for historical purposes.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="remarks")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    text = models.TextField()

    class Meta:  # noqa: D106
        db_table = "metis_rel_remark"

    def save(self, *args, **kwargs):
        """Save the remark and create a snapshot of the object."""
        super().save(*args, **kwargs)
        save_snapshot(self.content_object.__class__, self.content_object, user=self.created_by)  # type: ignore


class RemarksMixin(models.Model):
    """Mixin for models that can have remarks."""

    remarks = GenericRelation(Remark)

    class Meta:  # noqa: D106
        abstract = True


@receiver(post_save, sender=Remark)
def update_internship_tags(sender, instance, **kwargs):
    """Update the tags of the associated internship when an evaluation is saved."""
    from metis.models.stages.internships import Internship

    if isinstance(instance.content_object, Internship):
        Internship.update_tags(instance.content_object, type="remarks")
