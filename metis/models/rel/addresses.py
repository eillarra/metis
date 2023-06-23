from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_countries.fields import CountryField

from metis.services.mapbox import MapboxFeature


class Address(models.Model):
    """
    A physical address.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="addresses")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    address = models.CharField(max_length=160)
    city = models.CharField(max_length=40)
    postcode = models.CharField(max_length=16)
    country = CountryField()
    mapbox_feature = models.JSONField(null=True, blank=True)
    label = models.CharField(max_length=160, null=True, blank=True)

    class Meta:
        db_table = "metis_rel_address"

    @property
    def feature(self) -> MapboxFeature | None:
        return MapboxFeature(self.mapbox_feature) if self.mapbox_feature else None

    @property
    def full_address(self) -> str:
        return self.feature.full_address if self.feature else f"{self.address}, {self.postcode} {self.city}"


class AddressesMixin(models.Model):
    addresses = GenericRelation(Address)

    class Meta:
        abstract = True
