from rest_framework import serializers

from metis.models import Internship
from ..base import BaseModelSerializer, NestedHyperlinkField
from ..rel.remarks import RemarksMixin
from .programs import ProgramInternshipSerializer


project_internship_lookup_fields = {
    "parent_lookup_education_id": "project__education_id",
    "parent_lookup_project_id": "project_id",
}


class InternshipSerializer(RemarksMixin, BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-internship-detail", nested_lookup=project_internship_lookup_fields)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    program_internship = ProgramInternshipSerializer(read_only=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    custom_start_date = serializers.DateField(allow_null=True, required=False)
    custom_end_date = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = Internship
        exclude = ("created_at", "created_by")
