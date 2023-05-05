from rest_framework import serializers

from metis.models.stages.programs import Program, ProgramBlock, ProgramInternship, Track
from ..base import BaseModelSerializer


class TrackTinySerializer(BaseModelSerializer):
    class Meta:
        model = Track
        fields = ("id", "name", "program")


class TrackSerializer(BaseModelSerializer):
    class Meta:
        model = Track
        exclude = ("created_at", "created_by")


class ProgramInternshipTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramInternship
        exclude = ("created_at", "created_by")


class ProgramBlockTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramBlock
        fields = ("id", "name", "position", "program")


class ProgramBlockSerializer(serializers.ModelSerializer):
    internships = ProgramInternshipTinySerializer(many=True, read_only=True)

    class Meta:
        model = ProgramBlock
        fields = ("id", "name", "position", "internships")


class ProgramInternshipSerializer(serializers.ModelSerializer):
    block = ProgramBlockTinySerializer(read_only=True)

    class Meta:
        model = ProgramInternship
        exclude = ("created_at", "created_by")


class ProgramSerializer(BaseModelSerializer):
    education = serializers.HyperlinkedRelatedField(view_name="v1:education-detail", read_only=True)
    blocks = ProgramBlockSerializer(many=True, read_only=True)
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        exclude = ("created_at", "created_by")
