from rest_framework import serializers

from metis.models.stages.internships import Internship, Mentor

from ..base import BaseModelSerializer, NestedHyperlinkField
from ..disciplines import DisciplineSerializer
from ..places import PlaceInertiaSerializer
from ..rel.remarks import RemarksMixin
from ..users import UserLastLoginSerializer
from .evaluations import EvaluationFormSerializer
from .projects import PeriodSerializer, ProjectSerializer
from .students import StudentInertiaSerializer


project_lookup_fields = {
    "parent_lookup_education_id": "project__education_id",
    "parent_lookup_project_id": "project_id",
}
internship_lookup_fields = {
    "parent_lookup_education_id": "project__education_id",
    "parent_lookup_project_id": "project_id",
    "parent_lookup_internship_id": "id",
}


class MentorTinySerializer(BaseModelSerializer):
    user = UserLastLoginSerializer(read_only=True)

    class Meta:
        model = Mentor
        fields = ("id", "user")


class InternshipSerializer(RemarksMixin, BaseModelSerializer):
    """Internship serializer."""

    self = NestedHyperlinkField("v1:project-internship-detail", nested_lookup=project_lookup_fields)
    rel_absences = NestedHyperlinkField("v1:project-internship-absence-list", nested_lookup=internship_lookup_fields)
    rel_evaluations = NestedHyperlinkField(
        "v1:project-internship-evaluation-list", nested_lookup=internship_lookup_fields
    )
    rel_timesheets = NestedHyperlinkField(
        "v1:project-internship-timesheet-list", nested_lookup=internship_lookup_fields
    )
    uuid = serializers.UUIDField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    mentors = MentorTinySerializer(many=True, read_only=True)

    class Meta:  # noqa: D106
        model = Internship
        exclude = ("created_at", "created_by")


class InternshipInertiaSerializer(InternshipSerializer):
    """Internship serializer for Inertia."""

    Discipline = DisciplineSerializer(read_only=True, source="discipline")
    Period = PeriodSerializer(read_only=True, source="period")
    Student = StudentInertiaSerializer(read_only=True, source="student")
    EvaluationForm = EvaluationFormSerializer(read_only=True, source="evaluation_form")


class InternshipFullInertiaSerializer(InternshipInertiaSerializer):
    """Internship serializer for Inertia, with nested place."""

    Place = PlaceInertiaSerializer(read_only=True, source="place")


class PreplanningInternshipSerializer(InternshipFullInertiaSerializer):
    """Internship serializer for preplanning."""

    Project = ProjectSerializer(read_only=True, source="project")
