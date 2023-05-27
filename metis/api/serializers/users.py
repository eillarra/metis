from rest_framework import serializers

from metis.models.users import User


class UserTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "username", "email", "is_active", "last_login", "date_joined")
