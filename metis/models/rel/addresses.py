from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_countries.fields import CountryField


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

    class Meta:
        db_table = "metis_rel_address"


class AddressesMixin(models.Model):
    addresses = GenericRelation(Address)

    class Meta:
        abstract = True
