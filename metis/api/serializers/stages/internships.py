from rest_framework import serializers

from metis.models.stages.internships import Internship
from ..base import BaseModelSerializer, NestedHyperlinkField
from ..disciplines import DisciplineSerializer
from ..rel.remarks import RemarksMixin
from .programs import ProgramInternshipSerializer, TrackTinySerializer


project_internship_lookup_fields = {
    "parent_lookup_education_id": "period__project__education_id",
    "parent_lookup_project_id": "period__project_id",
}


class InternshipSerializer(RemarksMixin, BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-internship-detail", nested_lookup=project_internship_lookup_fields)
    program_internship = ProgramInternshipSerializer(read_only=True)
    track = TrackTinySerializer(read_only=True)
    discipline = DisciplineSerializer()
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    custom_start_date = serializers.DateField(allow_null=True)
    custom_end_date = serializers.DateField(allow_null=True)

    class Meta:
        model = Internship
        exclude = ("created_at", "created_by")
