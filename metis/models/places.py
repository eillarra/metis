from django.db import models
from django_countries.fields import CountryField
from modeltranslation.translator import TranslationOptions
from typing import TYPE_CHECKING

from .base import BaseModel
from .rel import AddressesMixin, FilesMixin, LinksMixin, PhoneNumbersMixin, RemarksMixin, TextEntriesMixin

if TYPE_CHECKING:
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


class Place(AddressesMixin, FilesMixin, PhoneNumbersMixin, LinksMixin, RemarksMixin, TextEntriesMixin, BaseModel):
    """
    The stagebureau works with their own list of places.
    Contacts or remarks are specific to each Education.
    """

    HOSPITAL = "hospital"
    WARD = "ward"
    PRIVATE = "private_center"
    TYPES = (
        (HOSPITAL, "Hospital"),
        (WARD, "Ward"),
        (PRIVATE, "Private center"),
    )

    education = models.ForeignKey("metis.Education", related_name="places", on_delete=models.PROTECT)
    type = models.CharField(max_length=16, choices=TYPES, default=HOSPITAL)
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=160)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, related_name="places", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "metis_education_places"
        ordering = ["education", "code"]
        unique_together = ("education", "code")

    def __str__(self) -> str:
        return self.name

    def can_be_managed_by(self, user) -> bool:
        return self.education.can_be_managed_by(user)

    @property
    def agreement(self) -> "File":
        return self.get_file("agreement")

    @property
    def is_hospital(self) -> bool:
        return self.type == self.HOSPITAL

    @property
    def is_ward(self) -> bool:
        return self.type == self.WARD

    @property
    def is_private(self) -> bool:
        return self.type == self.PRIVATE


class Contact(PhoneNumbersMixin, RemarksMixin, BaseModel):
    """
    Contact information for a place.
    Contacts can have administrative rights for a place for a education (`is_staff`).
    Contacts can also be designed as mentors. These mentors can be then assigned to specific internships.
    Contacts that are no staff or mentor have limited read-only access to the place information.
    """

    place = models.ForeignKey(Place, related_name="contacts", on_delete=models.CASCADE)
    user = models.ForeignKey("metis.User", related_name="contact_set", on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=True)

    class Meta:
        db_table = "metis_education_contacts"
        unique_together = ("place", "user")

    def __str__(self) -> str:
        return f"{self.user} ({self.place.code})"

    def can_be_managed_by(self, user) -> bool:
        return self.place.can_be_managed_by(user)
