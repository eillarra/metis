from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_countries.fields import CountryField


class Address(models.Model):
    """
    A physical address.
    TODO: include Mapbox-specific information?
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="addresses")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = CountryField()

    class Meta:
        db_table = "epione_rel_address"


class AddressesMixin(models.Model):
    addresses = GenericRelation(Address)

    class Meta:
        abstract = True
