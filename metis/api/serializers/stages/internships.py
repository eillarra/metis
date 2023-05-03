from metis.models.stages.internships import Internship
from ..base import BaseModelSerializer
from ..disciplines import DisciplineSerializer
from .programs import ProgramInternshipSerializer, TrackTinySerializer


class InternshipSerializer(BaseModelSerializer):
    program_internship = ProgramInternshipSerializer(read_only=True)
    track = TrackTinySerializer(read_only=True)
    discipline = DisciplineSerializer()

    class Meta:
        model = Internship
        exclude = ("created_at", "created_by")
