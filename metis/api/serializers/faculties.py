from rest_framework import serializers

from metis.models.faculties import Education, Faculty
from .base import BaseModelSerializer
from .users import UserTinySerializer


class FacultySerializer(BaseModelSerializer):
    class Meta:
        model = Faculty
        exclude = ("created_at", "created_by")


class EducationSerializer(BaseModelSerializer):
    url = serializers.URLField(source="get_office_url", read_only=True)
    self = serializers.HyperlinkedIdentityField(view_name="v1:education-detail", read_only=True)
    rel_programs = serializers.HyperlinkedIdentityField(view_name="v1:education-programs", read_only=True)
    rel_projects = serializers.HyperlinkedIdentityField(view_name="v1:education-projects", read_only=True)
    faculty = FacultySerializer(read_only=True)
    office_members = UserTinySerializer(many=True, read_only=True)

    class Meta:
        model = Education
        exclude = ("created_at", "created_by")
        depth = 1
