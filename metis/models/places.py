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
