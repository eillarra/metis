from rest_framework import serializers

from metis.models.stages.internships import Internship, Mentor
from ..base import BaseModelSerializer, NestedHyperlinkField
from ..disciplines import DisciplineSerializer
from ..rel.remarks import RemarksMixin
from ..users import UserLastLoginSerializer
from .programs import ProgramInternshipSerializer
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
    self = NestedHyperlinkField("v1:project-internship-detail", nested_lookup=project_lookup_fields)
    rel_absences = NestedHyperlinkField("v1:project-internship-absence-list", nested_lookup=internship_lookup_fields)
    rel_timesheets = NestedHyperlinkField(
        "v1:project-internship-timesheet-list", nested_lookup=internship_lookup_fields
    )
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    program_internship = ProgramInternshipSerializer(read_only=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    custom_start_date = serializers.DateField(allow_null=True, required=False)
    custom_end_date = serializers.DateField(allow_null=True, required=False)
    mentors = MentorTinySerializer(many=True, read_only=True)

    class Meta:
        model = Internship
        exclude = ("created_at", "created_by")


class InternshipInertiaSerializer(InternshipSerializer):
    Discipline = DisciplineSerializer(read_only=True, source="discipline")
    Student = StudentInertiaSerializer(read_only=True, source="student")
