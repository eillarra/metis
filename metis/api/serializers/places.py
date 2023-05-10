from rest_framework import serializers

from metis.models.places import Region, Place
from .base import BaseModelSerializer
from .rel.remarks import RemarksMixin


class RegionSerializer(BaseModelSerializer):
    updated_by = None

    class Meta:
        model = Region
        fields = ("id", "name", "country")


class PlaceSerializer(RemarksMixin, BaseModelSerializer):
    self = serializers.HyperlinkedIdentityField(view_name="v1:place-detail", read_only=True)
    parent = serializers.HyperlinkedRelatedField(view_name="v1:place-detail", read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Place
        exclude = ("created_at", "created_by")
