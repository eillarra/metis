from rest_framework import serializers

from metis.models import ProgramBlock, User, Student
from ..base import BaseModelSerializer, NestedHyperlinkField
from ..rel.remarks import RemarksMixin
from .projects import ProjectTinySerializer
from .programs import ProgramBlockSerializer


project_student_lookup_fields = {
    "parent_lookup_education_id": "project__education_id",
    "parent_lookup_project_id": "project_id",
}


class StudentSerializer(RemarksMixin, BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-student-detail", nested_lookup=project_student_lookup_fields)
    project = ProjectTinySerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)
    block = ProgramBlockSerializer(read_only=True)
    block_id = serializers.PrimaryKeyRelatedField(source="block", queryset=ProgramBlock.objects.all(), write_only=True)

    class Meta:
        model = Student
        exclude = ("created_at", "created_by")


class StudentUserSerializer(serializers.ModelSerializer):
    student_set = StudentSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "name", "email", "last_login", "is_active", "student_set")
