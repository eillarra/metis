from rest_framework import serializers

from metis.models.rel.addresses import Address
from .base import RelHyperlinkedField, NestedRelHyperlinkField


class AddressSerializer(serializers.ModelSerializer):
    self = NestedRelHyperlinkField(view_name="v1:address-detail")

    class Meta:
        model = Address
        exclude = (
            "content_type",
            "object_id",
        )


class AddressesMixin(serializers.ModelSerializer):
    rel_addresses = RelHyperlinkedField(view_name="v1:address-list")
