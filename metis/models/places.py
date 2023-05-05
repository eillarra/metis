from django.db import models
from django_countries.fields import CountryField
from modeltranslation.translator import TranslationOptions
from typing import Optional

from .base import BaseModel
from .rel.addresses import AddressesMixin
from .rel.links import LinksMixin
from .rel.phone_numbers import PhoneNumbersMixin
from .rel.remarks import RemarksMixin


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


class Place(AddressesMixin, PhoneNumbersMixin, LinksMixin, RemarksMixin, BaseModel):
    HOSPITAL = "hospital"
    WARD = "ward"
    PRIVATE = "private_center"
    TYPES = (
        (HOSPITAL, "Hospital"),
        (WARD, "Ward"),
        (PRIVATE, "Private center"),
    )

    type = models.CharField(max_length=16, choices=TYPES, default=HOSPITAL)
    name = models.CharField(max_length=160)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, related_name="places", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["type", "name"]

    def __str__(self) -> str:
        return self.name

    @property
    def is_hospital(self) -> bool:
        return self.type == self.HOSPITAL

    @property
    def is_ward(self) -> bool:
        return self.type == self.WARD

    @property
    def is_private(self) -> bool:
        return self.type == self.PRIVATE

    @property
    def cities(self) -> Optional[str]:
        return ", ".join([address.city for address in self.addresses.all()])


class EducationPlace(RemarksMixin, BaseModel):
    """
    The stagebureau works with a subset of all the places available.
    Contacts or remarks are specific to each Education.
    """

    education = models.ForeignKey("metis.Education", related_name="place_set", on_delete=models.PROTECT)
    place = models.ForeignKey("metis.Place", on_delete=models.CASCADE)
    code = models.CharField(max_length=160)

    class Meta:
        db_table = "metis_education_places"
        unique_together = (("education", "place"), ("education", "code"))

    def __str__(self) -> str:
        return f"{self.code} ({self.education.code})"


class Contact(PhoneNumbersMixin, RemarksMixin, BaseModel):
    """
    Contact information for a place.
    Contacts can have administrative rights for a place for a education (`is_staff`).
    Contacts can also be designed as mentors. These mentors can be then assigned to specific internships.
    Contacts that are no staff or mentor have limited read-only access to the place information.
    """

    place = models.ForeignKey(EducationPlace, related_name="contacts", on_delete=models.CASCADE)
    user = models.ForeignKey("metis.User", related_name="contact_objects", on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=True)

    class Meta:
        db_table = "metis_education_contacts"
        unique_together = ("place", "user")

    def __str__(self) -> str:
        return f"{self.user} ({self.place.code})"
