from rest_framework import serializers

from metis.models import User, Student
from .projects import ProjectTinySerializer
from .programs import ProgramBlockTinySerializer


class StudentObjectSerializer(serializers.ModelSerializer):
    project = ProjectTinySerializer()
    block = ProgramBlockTinySerializer()

    class Meta:
        model = Student
        exclude = ("user", "created_at", "created_by", "updated_at", "updated_by")


class StudentSerializer(serializers.ModelSerializer):
    student_objects = StudentObjectSerializer(many=True)

    class Meta:
        model = User
        fields = ("username", "name", "email", "last_login", "is_active", "student_objects")
