from rest_framework import serializers

from metis.models.stages.projects import Project
from ..base import BaseModelSerializer


class ProjectTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name")


class ProjectSerializer(BaseModelSerializer):
    self = serializers.HyperlinkedIdentityField(view_name="v1:project-detail", read_only=True)
    rel_places = serializers.HyperlinkedIdentityField(view_name="v1:project-places", read_only=True)
    rel_students = serializers.HyperlinkedIdentityField(view_name="v1:project-students", read_only=True)
    education = serializers.HyperlinkedRelatedField(view_name="v1:education-detail", read_only=True)
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)

    class Meta:
        model = Project
        exclude = ("created_at", "created_by", "places")
        depth = 1
