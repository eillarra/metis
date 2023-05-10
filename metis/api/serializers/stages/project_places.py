from rest_framework import serializers

from metis.models import Discipline, EducationPlace, ProjectPlace
from ..base import BaseModelSerializer, NestedHyperlinkField
from ..disciplines import DisciplineSerializer
from ..places import PlaceSerializer


project_lookup_fields = {
    "parent_lookup_education_id": "education_place__education_id",
}
project_place_lookup_fields = {
    "parent_lookup_education_id": "education_place__education_id",
    "parent_lookup_project_id": "project_id",
}


class ProjectPlaceSerializer(BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-place-detail", nested_lookup=project_place_lookup_fields)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    education_place = serializers.PrimaryKeyRelatedField(read_only=True)
    education_place_id = serializers.PrimaryKeyRelatedField(
        source="education_place", queryset=EducationPlace.objects.all(), write_only=True
    )
    place = PlaceSerializer(read_only=True)
    disciplines = DisciplineSerializer(many=True, read_only=True)
    discipline_ids = serializers.PrimaryKeyRelatedField(
        source="disciplines", queryset=Discipline.objects.all(), write_only=True, many=True, required=False
    )

    class Meta:
        model = ProjectPlace
        exclude = ("created_at", "created_by")
