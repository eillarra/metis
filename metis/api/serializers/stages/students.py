from rest_framework import serializers

from metis.models import User, Student
from .projects import ProjectTinySerializer
from .programs import ProgramBlockTinySerializer


class StudentRecord(serializers.ModelSerializer):
    project = ProjectTinySerializer()
    block = ProgramBlockTinySerializer()

    class Meta:
        model = Student
        exclude = ("user", "created_at", "created_by", "updated_at", "updated_by")


class StudentSerializer(serializers.ModelSerializer):
    student_records = StudentRecord(many=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "last_login", "is_active", "student_records")
