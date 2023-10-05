from rest_framework import serializers

from metis.models import Place, PlaceType, Contact, User
from .base import BaseTranslatedModelSerializer, BaseModelSerializer, NestedHyperlinkField
from .rel import AddressSerializer, AddressesMixin, RemarksMixin, TextEntriesMixin
from .users import UserLastLoginSerializer


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
    self = NestedHyperlinkField("v1:education-place-contact-detail", nested_lookup=education_place_lookup_fields)
    user = UserLastLoginSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)
    place = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contact
        exclude = ("created_at", "created_by")


class PlaceSerializer(AddressesMixin, RemarksMixin, TextEntriesMixin, BaseModelSerializer):
    self = NestedHyperlinkField("v1:education-place-detail", nested_lookup=education_lookup_fields)
    rel_contacts = NestedHyperlinkField("v1:education-place-contact-list", nested_lookup=education_lookup_fields_pk)
    education = serializers.PrimaryKeyRelatedField(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        exclude = ("created_at", "created_by")


class PlaceTypeSerializer(BaseTranslatedModelSerializer):
    class Meta:
        model = PlaceType
        fields = ("id", "name")


class PlaceInertiaSerializer(PlaceSerializer):
    Type = PlaceTypeSerializer(read_only=True, source="type")
    addresses = AddressSerializer(many=True, read_only=True)
