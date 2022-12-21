from django.db import models

from .base import BaseModel
from .links import LinksMixin


class Place(LinksMixin, BaseModel):
    HOSPITAL = "hospital"
    WARD = "ward"
    PRIVATE = "private_center"
    TYPE_CHOICES = (
        (HOSPITAL, "Hospital"),
        (WARD, "Ward"),
        (PRIVATE, "Private center"),
    )

    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default=HOSPITAL)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, null=True, blank=True)

    disciplines = models.ManyToManyField("sparta.Discipline", related_name="places")

    def __str__(self) -> str:
        return self.name
