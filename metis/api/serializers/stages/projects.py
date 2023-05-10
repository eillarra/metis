from rest_framework import serializers

from metis.models.stages.projects import Project
from ..base import BaseModelSerializer, NestedHyperlinkField


parent_lookup_fields = {
    "parent_lookup_education_id": "education_id",
}


class ProjectTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name")


class ProjectSerializer(BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-detail", nested_lookup=parent_lookup_fields)
    rel_internships = NestedHyperlinkField("v1:project-internships", nested_lookup=parent_lookup_fields)
    rel_places = NestedHyperlinkField("v1:project-places", nested_lookup=parent_lookup_fields)
    rel_students = NestedHyperlinkField("v1:project-students", nested_lookup=parent_lookup_fields)
    education = serializers.HyperlinkedRelatedField(view_name="v1:education-detail", read_only=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)

    class Meta:
        model = Project
        exclude = ("created_at", "created_by", "education_places")
