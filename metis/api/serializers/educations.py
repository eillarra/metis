from rest_framework import serializers

from metis.models.educations import Education, Faculty

from .base import BaseTranslatedModelSerializer
from .disciplines import DisciplineSerializer
from .places import PlaceLocationSerializer, PlaceTypeSerializer
from .users import UserTinySerializer


class FacultySerializer(BaseTranslatedModelSerializer):
    """Serializer for the Faculty model."""

    class Meta:  # noqa: D106
        model = Faculty
        exclude = ["created_at", "created_by"]


class EducationTinySerializer(serializers.ModelSerializer):
    """Tiny serializer for the Education model."""

    configuration = serializers.JSONField(read_only=True)

    class Meta:  # noqa: D106
        model = Education
        fields = ["id", "code", "short_name", "office_email", "configuration"]


class EducationSerializer(BaseTranslatedModelSerializer):
    """Serializer for the Education model."""

    url = serializers.URLField(source="get_office_url", read_only=True)
    self = serializers.HyperlinkedIdentityField(view_name="v1:education-detail", read_only=True)
    rel_places = serializers.HyperlinkedIdentityField(
        view_name="v1:education-place-list", lookup_url_kwarg="parent_lookup_education_id", read_only=True
    )
    rel_programs = serializers.HyperlinkedIdentityField(view_name="v1:education-programs", read_only=True)
    rel_projects = serializers.HyperlinkedIdentityField(
        view_name="v1:project-list", lookup_url_kwarg="parent_lookup_education_id", read_only=True
    )
    faculty = FacultySerializer(read_only=True)
    office_members = UserTinySerializer(many=True)
    disciplines = DisciplineSerializer(many=True)
    configuration = serializers.JSONField(read_only=True)
    place_locations = PlaceLocationSerializer(many=True, read_only=True)
    place_types = PlaceTypeSerializer(many=True, read_only=True)

    class Meta:  # noqa: D106
        model = Education
        exclude = ["config", "created_at", "created_by"]
