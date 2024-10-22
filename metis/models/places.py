from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from modeltranslation.translator import TranslationOptions

from .base import BaseModel, TagsMixin
from .rel import (
    AddressesMixin,
    FilesMixin,
    LinksMixin,
    PhoneNumbersMixin,
    RemarksMixin,
    TextEntriesMixin,
    append_files_tags,
    append_remarks_tags,
)


if TYPE_CHECKING:
    from .educations import Education


def get_place_tags(obj: "Place", *, type: str = "all") -> list[str]:
    """For an internship, process the tags.

    :param obj: An instance of the Place class.
    :param type: The type of tags to process.
    :returns: A list of tags.
    """
    tags = obj.tags

    # files
    if type in {"all", "files"}:
        tags = append_files_tags(obj, tags=tags)

    # remarks
    if type in {"all", "remarks"}:
        tags = append_remarks_tags(obj, tags=tags)

    return list(set(tags))


class PlaceLocation(BaseModel):
    """Place locations are used to group places for a education."""

    education = models.ForeignKey("metis.Education", related_name="place_locations", on_delete=models.CASCADE)
    code = models.CharField(max_length=160)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:  # noqa: D106
        db_table = "metis_education_place_locations"
        unique_together = ["education", "code"]
        ordering = ["education", "position", "name"]

    def __str__(self) -> str:
        return self.name


class PlaceType(BaseModel):
    """Place types are used to group places for a education."""

    education = models.ForeignKey("metis.Education", related_name="place_types", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:  # noqa: D106
        db_table = "metis_education_place_types"
        unique_together = ["education", "name"]
        ordering = ["education", "position", "name"]

    def __str__(self) -> str:
        return self.name


class PlaceTypeTranslationOptions(TranslationOptions):
    """Translation options for PlaceType."""

    fields = ("name",)


class Place(
    AddressesMixin, FilesMixin, PhoneNumbersMixin, LinksMixin, RemarksMixin, TagsMixin, TextEntriesMixin, BaseModel
):
    """Places where internships can be done.

    This collection of places is specific to each education, so are the contacts and remarks.
    """

    education = models.ForeignKey("metis.Education", related_name="places", on_delete=models.PROTECT)
    location = models.ForeignKey(
        "metis.PlaceLocation", related_name="places", on_delete=models.SET_NULL, null=True, blank=True
    )
    type = models.ForeignKey("metis.PlaceType", related_name="places", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=160)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.SET_NULL, null=True, blank=True)
    is_flagged = models.BooleanField(default=False)
    default_language = models.CharField(max_length=2, default="nl")

    class Meta:  # noqa: D106
        db_table = "metis_education_places"
        ordering = ["education", "code"]
        unique_together = ("education", "code")

    def clean(self) -> None:
        """Validate that the parent and type are in the same education."""
        if self.parent and self.parent.education != self.education:
            raise ValidationError("Parent place must be in the same education.")
        if self.location and self.location.education != self.education:
            raise ValidationError("Place location must be in the same education.")
        if self.type and self.type.education != self.education:
            raise ValidationError("Place type must be in the same education.")

    @classmethod
    def update_tags(cls, place: "Place", *, type: str = "all") -> None:
        """Update tags for a place, without calling clean() on the model."""
        tags = get_place_tags(place, type=type)
        cls.objects.filter(id=place.id).update(tags=tags)

    def __str__(self) -> str:
        return self.name

    def user_is_admin(self, user) -> bool:
        """Check if the user is admin for this place."""
        return self.admins.filter(user=user).exists()

    def can_be_managed_by(self, user) -> bool:
        """Check if the user can manage this place."""
        return self.education.can_be_managed_by(user) or self.user_is_admin(user)

    def get_office_url(self) -> str:
        """Get the URL to the office view of the place."""
        return reverse("place_office", args=[self.pk])

    @property
    def admins(self) -> models.QuerySet:
        """The admin contacts for the place."""
        return self.contacts.filter(is_admin=True)  # type: ignore


def find_place_by_name(name: str, education: "Education") -> Place | None:
    """Find a place by name."""
    try:
        return Place.objects.get(name=name, education=education)
    except Place.DoesNotExist:
        return None


class Contact(PhoneNumbersMixin, RemarksMixin, BaseModel):
    """Contact information for a place.

    Contacts can have administrative rights for a place for a education (`is_staff`).
    Contacts can also be designed as mentors. These mentors can be then assigned to specific internships.
    Contacts that are no staff or mentor have limited read-only access to the place information.
    """

    place = models.ForeignKey("metis.Place", related_name="contacts", on_delete=models.CASCADE)
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
        """Set `is_staff` if `is_admin` is True."""
        if self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)

    def can_be_managed_by(self, user) -> bool:
        """Check if the user can manage this contact."""
        return self.place.can_be_managed_by(user)

    @property
    def education(self) -> "Education":
        """The education of the place."""
        return self.place.education
