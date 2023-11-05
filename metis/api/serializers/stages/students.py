from rest_framework import serializers

from metis.models import Student, User

from ..base import BaseModelSerializer, NestedHyperlinkField
from ..rel.addresses import AddressesMixin
from ..rel.forms import FormResponsesMixin
from ..rel.remarks import RemarksMixin
from ..users import UserLastLoginSerializer


project_lookup_fields = {
    "parent_lookup_education_id": "project__education_id",
    "parent_lookup_project_id": "project_id",
}


class StudentSerializer(FormResponsesMixin, RemarksMixin, BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-student-detail", nested_lookup=project_lookup_fields)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Student
        exclude = ("created_at", "created_by")


class StudentUserSerializer(AddressesMixin, serializers.ModelSerializer):
    student_set = StudentSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "rel_addresses", "username", "name", "email", "last_login", "is_active", "student_set")


class StudentInertiaSerializer(StudentSerializer):
    User = UserLastLoginSerializer(read_only=True, source="user")
