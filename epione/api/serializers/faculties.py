from rest_framework import serializers

from epione.models.faculties import Education, Faculty
from .base import BaseModelSerializer


class FacultySerializer(BaseModelSerializer):

    class Meta:
        model = Faculty
        exclude = ("created_at", "created_by")


class EducationSerializer(BaseModelSerializer):
    self = serializers.HyperlinkedIdentityField(view_name="v1:education-detail", read_only=True)
    rel_projects = serializers.HyperlinkedIdentityField(view_name="v1:education-projects", read_only=True)
    faculty = FacultySerializer(read_only=True)

    class Meta:
        model = Education
        exclude = ("created_at", "created_by")
