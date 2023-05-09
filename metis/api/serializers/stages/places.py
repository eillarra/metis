from rest_framework import serializers

from metis.models.stages.project_places import ProjectPlace
from metis.models.education_places import EducationPlace
from ..base import BaseModelSerializer, NestedHyperlinkField
from ..disciplines import DisciplineSerializer
from ..places import PlaceSerializer


parent_lookup_fields = {
    "parent_lookup_education": "education_place__education_id",
    "parent_lookup_project": "project_id",
}


class ProjectPlaceSerializer(BaseModelSerializer):
    # self = NestedHyperlinkField("v1:project-place-detail", nested_lookup=parent_lookup_fields)
    place = PlaceSerializer(read_only=True)
    disciplines = DisciplineSerializer(many=True)

    class Meta:
        model = ProjectPlace
        exclude = ("created_at", "created_by")
