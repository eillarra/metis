from rest_framework import serializers

from metis.models.stages.projects import Project
from ..base import BaseModelSerializer


class ProjectSerializer(BaseModelSerializer):
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)

    class Meta:
        model = Project
        exclude = ("created_at", "created_by")
