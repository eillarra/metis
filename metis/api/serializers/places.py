from rest_framework import serializers

from metis.models.places import Region, Place
from .base import BaseModelSerializer
from .disciplines import DisciplineTinySerializer


class RegionSerializer(BaseModelSerializer):
    updated_by = None

    class Meta:
        model = Region
        exclude = ("wikidata_id", "updated_by", "updated_at", "created_at", "created_by")


class PlaceSerializer(BaseModelSerializer):
    self = serializers.HyperlinkedIdentityField(view_name="v1:place-detail", read_only=True)
    region = RegionSerializer(read_only=True)
    disciplines = DisciplineTinySerializer(many=True)

    class Meta:
        model = Place
        exclude = ("created_at", "created_by")
