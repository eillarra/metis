from rest_framework import serializers

from metis.models.stages.projects import Project, Period
from ..base import BaseModelSerializer, NestedHyperlinkField


education_lookup_fields = {
    "parent_lookup_education_id": "education_id",
}
project_lookup_fields = {
    "parent_lookup_education_id": "education_id",
    "parent_lookup_project_id": "id",
}


class PeriodSerializer(BaseModelSerializer):
    class Meta:
        model = Period
        exclude = ("created_at", "created_by", "project")


class ProjectTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name")


class ProjectSerializer(BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-detail", nested_lookup=education_lookup_fields)
    rel_internships = NestedHyperlinkField("v1:project-internship-list", nested_lookup=project_lookup_fields)
    rel_places = NestedHyperlinkField("v1:project-place-list", nested_lookup=project_lookup_fields)
    rel_students = NestedHyperlinkField("v1:project-student-users", nested_lookup=education_lookup_fields)
    education = serializers.PrimaryKeyRelatedField(read_only=True)
    periods = PeriodSerializer(many=True, read_only=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)

    class Meta:
        model = Project
        exclude = ("created_at", "created_by", "places")
