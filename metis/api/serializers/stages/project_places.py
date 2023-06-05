from rest_framework import serializers

from metis.models import Place, ProjectPlace
from ..base import BaseModelSerializer, NestedHyperlinkField
from ..places import PlaceSerializer
from ..rel.remarks import RemarksMixin


project_lookup_fields = {
    "parent_lookup_education_id": "place__education_id",
}
project_place_lookup_fields = {
    "parent_lookup_education_id": "place__education_id",
    "parent_lookup_project_id": "project_id",
}


class ProjectPlaceSerializer(RemarksMixin, BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-place-detail", nested_lookup=project_place_lookup_fields)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    place = PlaceSerializer(read_only=True)
    place_id = serializers.PrimaryKeyRelatedField(source="place", queryset=Place.objects.all(), write_only=True)

    class Meta:
        model = ProjectPlace
        exclude = ("created_at", "created_by")
