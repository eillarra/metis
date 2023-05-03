from rest_framework import serializers

from metis.models.institutions import Region, Institution
from .base import BaseModelSerializer


class RegionSerializer(BaseModelSerializer):
    updated_by = None

    class Meta:
        model = Region
        fields = ("id", "name", "country")


class InstitutionSerializer(BaseModelSerializer):
    self = serializers.HyperlinkedIdentityField(view_name="v1:institution-detail", read_only=True)
    parent = serializers.HyperlinkedRelatedField(view_name="v1:institution-detail", read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Institution
        exclude = ("created_at", "created_by")
