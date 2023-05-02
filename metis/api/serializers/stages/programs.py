from rest_framework import serializers

from metis.models.stages.programs import Program, ProgramBlock
from ..base import BaseModelSerializer


class ProgramBlockTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramBlock
        fields = ("id", "name", "position")


class ProgramSerializer(BaseModelSerializer):
    education = serializers.HyperlinkedRelatedField(view_name="v1:education-detail", read_only=True)
    blocks = ProgramBlockTinySerializer(many=True, read_only=True)

    class Meta:
        model = Program
        exclude = ("created_at", "created_by")
