from rest_framework import serializers

from metis.models.stages.internships import Internship
from ..base import BaseModelSerializer
from ..disciplines import DisciplineSerializer
from ..rel.remarks import RemarksMixin
from .programs import ProgramInternshipSerializer, TrackTinySerializer


class InternshipSerializer(RemarksMixin, BaseModelSerializer):
    program_internship = ProgramInternshipSerializer(read_only=True)
    track = TrackTinySerializer(read_only=True)
    discipline = DisciplineSerializer()
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    custom_start_date = serializers.DateField(write_only=True, required=False, allow_null=True)
    custom_end_date = serializers.DateField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Internship
        exclude = ("created_at", "created_by")
