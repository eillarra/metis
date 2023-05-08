from rest_framework import serializers

from metis.models.places import Place
from metis.models.education_places import EducationPlace, Contact
from .base import BaseModelSerializer, NestedHyperlinkField
from .places import PlaceSerializer
from .users import UserTinySerializer


education_lookup_fields = {"parent_lookup_education": "education_id"}


class ContactSerializer(BaseModelSerializer):
    user = UserTinySerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ("id", "user", "is_staff", "is_mentor")


class EducationPlaceSerializer(BaseModelSerializer):
    self = NestedHyperlinkField("v1:education-place-detail", nested_lookup=education_lookup_fields)
    education = serializers.HyperlinkedRelatedField(view_name="v1:education-detail", read_only=True)
    place_id = serializers.PrimaryKeyRelatedField(source="place", queryset=Place.objects.all(), write_only=True)
    place = PlaceSerializer(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = EducationPlace
        exclude = ("created_at", "created_by")
