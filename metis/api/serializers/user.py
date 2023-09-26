from rest_framework import serializers

from metis.models.stages import Student, Signature
from metis.models.users import User
from .rel.addresses import AddressesMixin
from .rel.forms import FormResponsesMixin
from .stages import ProgramBlockSerializer, ProjectTinySerializer


class AuthUserSerializer(AddressesMixin, serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        exclude = ("password", "first_name", "last_name")
        read_only_fields = ("is_staff", "is_superuser", "is_active", "date_joined", "last_login")


class AuthStudentSerializer(FormResponsesMixin, serializers.ModelSerializer):
    project = ProjectTinySerializer(read_only=True)
    block = ProgramBlockSerializer(read_only=True)
    has_signed_required_texts = serializers.BooleanField(read_only=True)
    user = AuthUserSerializer(read_only=True)

    class Meta:
        model = Student
        exclude = ("created_at", "created_by")


class AuthSignatureSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True, source="get_absolute_url")

    class Meta:
        model = Signature
        exclude = ("uuid",)
