from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class PhoneNumber(models.Model):
    """A phone number."""

    MOBILE = "mobile"
    LANDLINE = "landline"
    TYPES = (
        (MOBILE, "Mobile"),
        (LANDLINE, "Landline"),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="phone_numbers")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(max_length=16, choices=TYPES)
    number = models.CharField(max_length=24)

    class Meta:  # noqa: D106
        db_table = "metis_rel_phone_number"

    def __str__(self) -> str:
        return self.number


class PhoneNumbersMixin(models.Model):
    """Phone numbers mixin."""

    phone_numbers = GenericRelation(PhoneNumber)

    class Meta:  # noqa: D106
        abstract = True
