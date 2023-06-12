from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from hashlib import sha256
from typing import Optional, TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from metis.models import Education, Contact, User


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

    def send_email(self) -> None:
        from metis.services.mailer import send_invitation_email

        send_invitation_email(self, self.education)

    def get_absolute_url(self) -> str:
        return reverse("invitation", kwargs={"uuid": self.uuid, "secret": self.secret})

    @property
    def education(self) -> Optional["Education"]:
        types_with_education = {"existing_contact", "contact", "student"}
        if self.type in types_with_education:
            return self.content_object.education  # type: ignore
        return None

    @property
    def user(self) -> Optional["User"]:
        types_with_user = {"existing_contact"}
        if self.type in types_with_user:
            return self.content_object.user  # type: ignore
        return None

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


@receiver(post_save, sender=Invitation)
def invitation_post_save(sender, instance, created, **kwargs):
    """
    TODO: In some cases it is possible that an invitation is created instead of creating a student or contact directly.
    We check for exiting users and create the student/contact if necessary.

    Send an invitation email to the user
    """

    # if "contact" in type, send it
    if created and "contact" in instance.type:  # TODO: this should be sent for all types in the future
        instance.send_email()
