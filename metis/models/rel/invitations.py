from uuid import uuid4

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Invitation(models.Model):
    """
    An invitation to join the platform.
    We have different type of invitations right now:
    - "contact": inviting a Contact; after accepting they will be added to a Place (content_object is a Place)
    - "student": inviting a Student; after accepting they will be added to a Project (content_object is a Project)

    We can have more types in the future.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="invitations")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(max_length=32)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=160)
    email = models.EmailField()
    data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "metis_rel_invitation"
        unique_together = ("content_type", "object_id", "type", "email")


class InvitationsMixin(models.Model):
    invitations = GenericRelation(Invitation)

    class Meta:
        abstract = True
