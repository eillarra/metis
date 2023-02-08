from django.db import models

from .base import BaseModel
from .rel.links import LinksMixin
from .rel.remarks import RemarksMixin


class Place(LinksMixin, RemarksMixin, BaseModel):
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
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, null=True, blank=True)

    # adrress
    # contact info
    # contacts
    # Mapbox location information?

    disciplines = models.ManyToManyField("sparta.Discipline", related_name="places")

    def __str__(self) -> str:
        return self.name
