from rest_framework import serializers

from metis.models import Contact, Place, PlaceLocation, PlaceType, User

from .base import BaseModelSerializer, BaseTranslatedModelSerializer, NestedHyperlinkField
from .rel import AddressesMixin, AddressSerializer, FilesMixin, PhoneNumbersMixin, RemarksMixin, TextEntriesMixin
from .users import EmailAddressSerializer, UserLastLoginSerializer


education_lookup_fields = {
    "parent_lookup_education_id": "education_id",
}
education_lookup_fields_pk = {
    "parent_lookup_education_id": "education__id",
    "parent_lookup_place_id": "id",
}
education_place_lookup_fields = {
    "parent_lookup_education_id": "place__education_id",
    "parent_lookup_place_id": "place_id",
}


class ContactSerializer(RemarksMixin, BaseModelSerializer):
    """Contact serializer."""

    self = NestedHyperlinkField("v1:education-place-contact-detail", nested_lookup=education_place_lookup_fields)
    user = UserLastLoginSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)
    place = serializers.PrimaryKeyRelatedField(read_only=True)
    email_addresses = serializers.SerializerMethodField()

    class Meta:  # noqa: D106
        model = Contact
        exclude = ("created_at", "created_by")

    def get_email_addresses(self, obj):
        """Return the email addresses of the user."""
        return EmailAddressSerializer(obj.user.emailaddress_set.all(), many=True).data


class PlaceSerializer(
    AddressesMixin, FilesMixin, PhoneNumbersMixin, RemarksMixin, TextEntriesMixin, BaseModelSerializer
):
    """Place serializer."""

    self = NestedHyperlinkField("v1:education-place-detail", nested_lookup=education_lookup_fields)
    rel_contacts = NestedHyperlinkField("v1:education-place-contact-list", nested_lookup=education_lookup_fields_pk)
    education = serializers.PrimaryKeyRelatedField(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:  # noqa: D106
        model = Place
        exclude = ("created_at", "created_by")


class PlaceLocationSerializer(BaseTranslatedModelSerializer):
    """Place location serializer."""

    class Meta:  # noqa: D106
        model = PlaceLocation
        fields = ["id", "code", "name"]


class PlaceTypeSerializer(BaseTranslatedModelSerializer):
    """Place type serializer."""

    class Meta:  # noqa: D106
        model = PlaceType
        fields = ["id", "name"]


class PlaceInertiaSerializer(PlaceSerializer):
    """Place serializer used by Inertia."""

    Location = PlaceLocationSerializer(read_only=True, source="location")
    Type = PlaceTypeSerializer(read_only=True, source="type")
    addresses = AddressSerializer(many=True, read_only=True)
