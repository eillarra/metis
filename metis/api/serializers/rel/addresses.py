from rest_framework import serializers

from metis.models.rel.addresses import Address

from .base import NestedRelHyperlinkField, RelHyperlinkedField


class AddressSerializer(serializers.ModelSerializer):
    """Address serializer."""

    self = NestedRelHyperlinkField(view_name="v1:address-detail")

    class Meta:  # noqa: D106
        model = Address
        exclude = ("content_type", "object_id", "mapbox_feature")


class AddressesMixin(serializers.ModelSerializer):
    """Addresses mixin."""

    rel_addresses = RelHyperlinkedField(view_name="v1:address-list")
    addresses = AddressSerializer(many=True, read_only=True)
