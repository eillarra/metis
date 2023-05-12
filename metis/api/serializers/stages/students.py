from rest_framework import serializers

from metis.models import User, Student
from ..rel.remarks import RemarksMixin
from .projects import ProjectTinySerializer
from .programs import ProgramBlockSerializer


class StudentSetSerializer(RemarksMixin, serializers.ModelSerializer):
    project = ProjectTinySerializer()
    block = ProgramBlockSerializer()

    class Meta:
        model = Student
        exclude = ("user", "created_at", "created_by")


class StudentSerializer(serializers.ModelSerializer):
    student_set = StudentSetSerializer(many=True)

    class Meta:
        model = User
        fields = ("username", "name", "email", "last_login", "is_active", "student_set")
