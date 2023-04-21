from django.db import models

from .base import BaseModel
from .rel.addresses import AddressesMixin
from .rel.links import LinksMixin
from .rel.remarks import RemarksMixin


class Region(BaseModel):
    name = models.CharField(max_length=160)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Place(AddressesMixin, LinksMixin, RemarksMixin, BaseModel):
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

    practical_information = models.TextField(blank=True, null=True)
    disciplines = models.ManyToManyField("metis.Discipline", related_name="places")

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
