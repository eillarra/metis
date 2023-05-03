from rest_framework import serializers

from metis.models.users import User


class UserTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
