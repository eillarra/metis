from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.db import models
from typing import Type, TYPE_CHECKING

from metis.services.mailer import send_mail_to_admins

if TYPE_CHECKING:
    from metis.models.base import BaseModel
    from metis.models.users import User


class Snapshot(models.Model):
    """
    A copy of the object is saved here for historical purposes.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="snapshots")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    data = models.JSONField(null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("metis.User", on_delete=models.SET_NULL, null=True, editable=False)

    class Meta:
        db_table = "metis_rel_snapshot"


class SnapshotsMixin(models.Model):
    snapshots = GenericRelation(Snapshot)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Note that this mixin should only be used by BaseModel.
        """

        super().save(*args, **kwargs)
        save_snapshot(self.__class__, self, user=self.updated_by)


def save_snapshot(sender: Type["BaseModel"], instance: models.Model, *, user: "User") -> None:
    """
    Save a snapshot of a given Django model instance.

    This method is intended to be used as a signal handler for the `post_save` signal.
    It serializes the instance, creates a new Snapshot object, and saves the serialized
    data to the Snapshot object.

    Note that the user information has to be added to the original BaseModel instance
    via the Admin `save_model` method or to the serializer `create` method in the API.

    Args:
        sender (BaseModel): The class of the saved instance.
        instance (Model): The instance of the saved object.

    Returns:
        None
    """

    if sender == Snapshot:
        return

    snapshot = Snapshot()
    snapshot.content_object = instance
    snapshot.created_by = user

    try:
        snapshot.data = serialize("json", [instance])
    except Exception as e:
        send_mail_to_admins("Snapshot Error", f"Error while serializing {type(instance).__name__} #{instance.id}: {e}")
        snapshot.data = None

    snapshot.save()
