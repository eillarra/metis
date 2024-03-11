from rest_framework import serializers

from metis.models.stages.projects import Period, Project

from ..base import BaseModelSerializer, NestedHyperlinkField
from ..rel import TextEntriesMixin
from .questionings import QuestioningTinySerializer


education_lookup_fields = {
    "parent_lookup_education_id": "education_id",
}
project_lookup_fields = {
    "parent_lookup_education_id": "education_id",
    "parent_lookup_project_id": "id",
}


class PeriodSerializer(BaseModelSerializer):
    """Period serializer."""

    full_name = serializers.CharField(read_only=True)

    class Meta:  # noqa: D106
        model = Period
        exclude = ("created_at", "created_by", "project")


class ProjectTinySerializer(serializers.ModelSerializer):
    """Tiny project serializer."""

    full_name = serializers.CharField(read_only=True)

    class Meta:  # noqa: D106
        model = Project
        fields = ("id", "name", "full_name")


class ProjectSerializer(TextEntriesMixin, BaseModelSerializer):
    """Project serializer."""

    self = NestedHyperlinkField("v1:project-detail", nested_lookup=education_lookup_fields)
    rel_emails = NestedHyperlinkField("v1:project-email-list", nested_lookup=project_lookup_fields)
    rel_internships = NestedHyperlinkField("v1:project-internship-list", nested_lookup=project_lookup_fields)
    rel_places = NestedHyperlinkField("v1:project-place-list", nested_lookup=project_lookup_fields)
    rel_questionings = NestedHyperlinkField("v1:project-questioning-list", nested_lookup=project_lookup_fields)
    rel_students = NestedHyperlinkField("v1:project-student-users", nested_lookup=education_lookup_fields)
    education = serializers.PrimaryKeyRelatedField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    periods = PeriodSerializer(many=True, read_only=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    questionings = QuestioningTinySerializer(many=True, read_only=True)  # TODO: remove this and use separate endpoint

    class Meta:  # noqa: D106
        model = Project
        exclude = ("created_at", "created_by", "places")
