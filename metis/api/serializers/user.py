from rest_framework import serializers

from metis.models.stages import Student, Signature
from metis.models.users import User, TmpData
from .stages import ProgramBlockSerializer, ProgramInternshipTinySerializer, ProjectTinySerializer


class AuthUserTmpDataSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TmpData
        exclude = ()


class AuthUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    tmp_data = AuthUserTmpDataSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ("password", "first_name", "last_name")


class AuthStudentSerializer(serializers.ModelSerializer):
    project = ProjectTinySerializer(read_only=True)
    block = ProgramBlockSerializer(read_only=True)
    has_signed_required_texts = serializers.BooleanField(read_only=True)
    internships = ProgramInternshipTinySerializer(many=True, read_only=True)
    user = AuthUserSerializer(read_only=True)

    class Meta:
        model = Student
        exclude = ("created_at", "created_by")


class AuthSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = "__all__"
