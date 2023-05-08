from rest_framework import serializers

from metis.models.educations import Education, Faculty
from .base import BaseModelSerializer
from .disciplines import DisciplineSerializer
from .users import UserTinySerializer


class FacultySerializer(BaseModelSerializer):
    class Meta:
        model = Faculty
        exclude = ("created_at", "created_by")


class EducationSerializer(BaseModelSerializer):
    url = serializers.URLField(source="get_office_url", read_only=True)
    self = serializers.HyperlinkedIdentityField(view_name="v1:education-detail", read_only=True)
    rel_places = serializers.HyperlinkedIdentityField(
        view_name="v1:education-place-list", lookup_url_kwarg="parent_lookup_education", read_only=True
    )
    rel_programs = serializers.HyperlinkedIdentityField(view_name="v1:education-programs", read_only=True)
    rel_projects = serializers.HyperlinkedIdentityField(
        view_name="v1:education-project-list", lookup_url_kwarg="parent_lookup_education", read_only=True
    )
    faculty = FacultySerializer(read_only=True)
    office_members = UserTinySerializer(many=True)
    disciplines = DisciplineSerializer(many=True)

    class Meta:
        model = Education
        exclude = ("created_at", "created_by", "places")
        depth = 1
