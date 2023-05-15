from rest_framework import serializers

from metis.models import Education, Region, Place, Contact, User
from .base import BaseModelSerializer, NestedHyperlinkField
from .rel.remarks import RemarksMixin
from .users import UserTinySerializer


education_lookup_fields = {
    "parent_lookup_education_id": "education_id",
}
education_place_lookup_fields = {
    "parent_lookup_education_id": "place__education_id",
    "parent_lookup_place_id": "place_id",
}


class RegionSerializer(BaseModelSerializer):
    updated_by = None

    class Meta:
        model = Region
        fields = ("id", "name", "country")


class ContactTinySerializer(RemarksMixin, BaseModelSerializer):
    self = NestedHyperlinkField("v1:education-place-contact-detail", nested_lookup=education_place_lookup_fields)
    user = UserTinySerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ("id", "self", "rel_remarks", "remark_count", "user", "is_staff", "is_mentor")


class PlaceSerializer(RemarksMixin, BaseModelSerializer):
    self = NestedHyperlinkField("v1:education-place-detail", nested_lookup=education_lookup_fields)
    parent = NestedHyperlinkField(view_name="v1:education-place-detail", nested_lookup=education_lookup_fields)
    education = serializers.PrimaryKeyRelatedField(read_only=True)
    education_id = serializers.PrimaryKeyRelatedField(
        source="education", queryset=Education.objects.all(), write_only=True
    )
    region = RegionSerializer(read_only=True)
    contacts = ContactTinySerializer(many=True, read_only=True)

    class Meta:
        model = Place
        exclude = ("created_at", "created_by")


class ContactSerializer(ContactTinySerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)
    place = NestedHyperlinkField(
        "v1:education-place-detail",
        nested_lookup={
            "parent_lookup_education_id": "place__education_id",
        },
    )

    class Meta:
        model = Contact
        exclude = ("created_at", "created_by")
