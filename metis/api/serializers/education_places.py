from rest_framework import serializers

from metis.models.places import Place
from metis.models.education_places import EducationPlace, Contact
from metis.models.users import User
from .base import BaseModelSerializer, NestedHyperlinkField
from .places import PlaceSerializer
from .users import UserTinySerializer


education_lookup_fields = {
    "parent_lookup_education": "education_id",
}
education_place_lookup_fields = {
    "parent_lookup_education_place__education": "education_place__education_id",
    "parent_lookup_education_place": "education_place_id",
}


class ContactTinySerializer(BaseModelSerializer):
    self = NestedHyperlinkField("v1:education-place-contact-detail", nested_lookup=education_place_lookup_fields)
    user = UserTinySerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ("id", "self", "user", "is_staff", "is_mentor")


class EducationPlaceSerializer(BaseModelSerializer):
    self = NestedHyperlinkField("v1:education-place-detail", nested_lookup=education_lookup_fields)
    education = serializers.HyperlinkedRelatedField(view_name="v1:education-detail", read_only=True)
    place = PlaceSerializer(read_only=True)
    place_id = serializers.PrimaryKeyRelatedField(source="place", queryset=Place.objects.all(), write_only=True)
    contacts = ContactTinySerializer(many=True, read_only=True)

    class Meta:
        model = EducationPlace
        exclude = ("created_at", "created_by")


class ContactSerializer(ContactTinySerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)
    education_place = EducationPlaceSerializer(read_only=True)
    education_place_id = serializers.PrimaryKeyRelatedField(
        source="education_place", queryset=EducationPlace.objects.all(), write_only=True
    )

    class Meta:
        model = Contact
        exclude = ("created_at", "created_by")
