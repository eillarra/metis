from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from hashlib import sha256
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from metis.models import Contact


class Invitation(models.Model):
    """
    An invitation to join the platform.
    We have different type of invitations right now:
    - "existing_contact": these already exist as contacts in the database, we created users, but they never logged in
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

    def save(self, *args, **kwargs) -> None:
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def process(self, user) -> None:
        from metis.services.inviter import process_invitation

        process_invitation(self, user)

    def get_absolute_url(self) -> str:
        return reverse("invitation", kwargs={"uuid": self.uuid, "secret": self.secret})

    @property
    def secret(self) -> str:
        return sha256(f"{self.uuid}{settings.SECRET_KEY}".encode("utf-8")).hexdigest()

    @classmethod
    def from_existing_contact(cls, contact: "Contact") -> "Invitation":
        return cls.objects.create(
            content_object=contact,
            type="existing_contact",
            name=contact.user.name,
            email=contact.user.email,
        )


class InvitationsMixin(models.Model):
    invitations = GenericRelation(Invitation)

    class Meta:
        abstract = True
