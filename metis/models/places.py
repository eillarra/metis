from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from modeltranslation.translator import TranslationOptions
from typing import TYPE_CHECKING

from .base import BaseModel
from .rel import AddressesMixin, FilesMixin, LinksMixin, PhoneNumbersMixin, RemarksMixin, TextEntriesMixin

if TYPE_CHECKING:
    from .educations import Education
    from .rel.files import File


class Region(BaseModel):
    wikidata_id = models.CharField(max_length=16, db_index=True, null=True, blank=True)
    name = models.CharField(max_length=160)
    country = CountryField()

    class Meta:
        ordering = ["country", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.country})"


class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)


class PlaceType(BaseModel):
    education = models.ForeignKey("metis.Education", related_name="place_types", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "metis_education_place_types"
        ordering = ["education", "position", "name"]


class PlaceTypeTranslationOptions(TranslationOptions):
    fields = ("name",)


class Place(AddressesMixin, FilesMixin, PhoneNumbersMixin, LinksMixin, RemarksMixin, TextEntriesMixin, BaseModel):
    """
    The stagebureau works with their own list of places.
    Contacts or remarks are specific to each Education.
    """

    education = models.ForeignKey("metis.Education", related_name="places", on_delete=models.PROTECT)
    type = models.ForeignKey(PlaceType, related_name="places", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=160)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, related_name="places", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "metis_education_places"
        ordering = ["education", "code"]
        unique_together = ("education", "code")

    def clean(self):
        if self.parent and self.parent.education != self.education:
            raise ValidationError("Parent place must be in the same education.")
        if self.type and self.type.education != self.education:
            raise ValidationError("Place type must be in the same education.")

    def __str__(self) -> str:
        return self.name

    def can_be_managed_by(self, user) -> bool:
        return self.education.can_be_managed_by(user)

    def get_office_url(self) -> str:
        return reverse("place_office", args=[self.pk])

    @property
    def agreement(self) -> "File":
        return self.get_file("agreement")


class Contact(PhoneNumbersMixin, RemarksMixin, BaseModel):
    """
    Contact information for a place.
    Contacts can have administrative rights for a place for a education (`is_staff`).
    Contacts can also be designed as mentors. These mentors can be then assigned to specific internships.
    Contacts that are no staff or mentor have limited read-only access to the place information.
    """

    place = models.ForeignKey(Place, related_name="contacts", on_delete=models.CASCADE)
    user = models.ForeignKey("metis.User", related_name="contact_set", on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=True)

    class Meta:
        db_table = "metis_education_contacts"
        unique_together = ("place", "user")

    def __str__(self) -> str:
        return f"{self.user} ({self.place.code})"

    def save(self, *args, **kwargs) -> None:
        if self.is_admin:
            self.is_staff = True
        return super().save(*args, **kwargs)

    def can_be_managed_by(self, user) -> bool:
        return self.place.can_be_managed_by(user)

    @property
    def education(self) -> "Education":
        return self.place.education
