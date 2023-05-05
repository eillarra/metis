from rest_framework import serializers

from metis.models.places import Region, Place, EducationPlace, Contact
from .base import BaseModelSerializer
from .users import UserTinySerializer


class RegionSerializer(BaseModelSerializer):
    updated_by = None

    class Meta:
        model = Region
        fields = ("id", "name", "country")


class PlaceSerializer(BaseModelSerializer):
    self = serializers.HyperlinkedIdentityField(view_name="v1:place-detail", read_only=True)
    parent = serializers.HyperlinkedRelatedField(view_name="v1:place-detail", read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Place
        exclude = ("created_at", "created_by")


class ContactSerializer(BaseModelSerializer):
    user = UserTinySerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ("id", "user", "is_staff", "is_mentor")


class EducationPlaceSerializer(BaseModelSerializer):
    place = PlaceSerializer()
    contacts = ContactSerializer(many=True)

    class Meta:
        model = EducationPlace
        exclude = ("created_at", "created_by")
