from metis.models.stages.project_places import ProjectPlace
from ..base import BaseModelSerializer, NestedHyperlinkField
from ..disciplines import DisciplineSerializer
from ..places import PlaceSerializer


parent_lookup_fields = {
    "parent_lookup_education_id": "education_place__education_id",
    "parent_lookup_project_id": "project_id",
}


class ProjectPlaceSerializer(BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-place-detail", nested_lookup=parent_lookup_fields)
    education_place = NestedHyperlinkField(
        "v1:education-place-detail",
        nested_lookup={
            "parent_lookup_education_id": "education_place__education_id",
        },
    )
    place = PlaceSerializer(read_only=True)
    disciplines = DisciplineSerializer(many=True)

    class Meta:
        model = ProjectPlace
        exclude = ("created_at", "created_by")
