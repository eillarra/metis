from allauth.account.models import EmailAddress
from rest_framework import serializers

from metis.models.users import User


class EmailAddressSerializer(serializers.Serializer):
    """Serializer for email addresses."""

    email = serializers.EmailField()
    verified = serializers.BooleanField()
    primary = serializers.BooleanField()

    class Meta:  # noqa: D106
        model = EmailAddress
        fields = ("email", "verified", "primary")


class UserTinySerializer(serializers.ModelSerializer):
    """Tiny user serializer."""

    class Meta:  # noqa: D106
        model = User
        fields = ("id", "name", "email")


class UserLastLoginSerializer(serializers.ModelSerializer):
    """User serializer with last login."""

    class Meta:  # noqa: D106
        model = User
        fields = ("id", "name", "email", "last_login")


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:  # noqa: D106
        model = User
        fields = ("id", "name", "username", "email", "is_active", "last_login", "date_joined")
