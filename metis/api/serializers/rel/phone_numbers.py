from rest_framework import serializers

from metis.models.rel.phone_numbers import PhoneNumber

from .base import RelHyperlinkedField


class PhoneNumberSerializer(serializers.ModelSerializer):
    """Phone number serializer."""

    class Meta:  # noqa: D106
        model = PhoneNumber
        exclude = (
            "content_type",
            "object_id",
        )


class PhoneNumbersMixin(serializers.ModelSerializer):
    """Phone numbers mixin."""

    rel_phone_numbers = RelHyperlinkedField(view_name="v1:phone-number-list")
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)
