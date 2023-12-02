from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from modeltranslation.translator import TranslationOptions

from .base import BaseModel
from .rel import AddressesMixin, FilesMixin, LinksMixin, PhoneNumbersMixin, RemarksMixin, TextEntriesMixin


if TYPE_CHECKING:
    from .educations import Education
    from .rel.files import File


class PlaceType(BaseModel):
    """Place types are used to group places for a education."""

    education = models.ForeignKey("metis.Education", related_name="place_types", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:  # noqa: D106
        db_table = "metis_education_place_types"
        ordering = ["education", "position", "name"]


class PlaceTypeTranslationOptions(TranslationOptions):
    """Translation options for PlaceType."""

    fields = ("name",)


class Place(AddressesMixin, FilesMixin, PhoneNumbersMixin, LinksMixin, RemarksMixin, TextEntriesMixin, BaseModel):
    """Places where internships can be done.

    This collection of places is specific to each education, so are the contacts and remarks.
    """

    education = models.ForeignKey("metis.Education", related_name="places", on_delete=models.PROTECT)
    type = models.ForeignKey(PlaceType, related_name="places", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=160)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.SET_NULL, null=True, blank=True)
    is_flagged = models.BooleanField(default=False)

    class Meta:  # noqa: D106
        db_table = "metis_education_places"
        ordering = ["education", "code"]
        unique_together = ("education", "code")

    def clean(self) -> None:
        """Validate that the parent and type are in the same education."""
        if self.parent and self.parent.education != self.education:
            raise ValidationError("Parent place must be in the same education.")
        if self.type and self.type.education != self.education:
            raise ValidationError("Place type must be in the same education.")

    def __str__(self) -> str:
        return self.name

    def can_be_managed_by(self, user) -> bool:
        return self.education.can_be_managed_by(user) or self.contacts.filter(user=user, is_admin=True).exists()

    def get_office_url(self) -> str:
        return reverse("place_office", args=[self.pk])

    @property
    def agreement(self) -> "File":
        return self.get_file("agreement")


class Contact(PhoneNumbersMixin, RemarksMixin, BaseModel):
    """Contact information for a place.

    Contacts can have administrative rights for a place for a education (`is_staff`).
    Contacts can also be designed as mentors. These mentors can be then assigned to specific internships.
    Contacts that are no staff or mentor have limited read-only access to the place information.
    """

    place = models.ForeignKey(Place, related_name="contacts", on_delete=models.CASCADE)
    user = models.ForeignKey("metis.User", related_name="contact_set", on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=True)

    class Meta:  # noqa: D106
        db_table = "metis_education_contacts"
        unique_together = ("place", "user")

    def __str__(self) -> str:
        return f"{self.user} ({self.place.code})"

    def save(self, *args, **kwargs) -> None:
        if self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)

    def can_be_managed_by(self, user) -> bool:
        return self.place.can_be_managed_by(user)

    @property
    def education(self) -> "Education":
        """The education of the place."""
        return self.place.education
