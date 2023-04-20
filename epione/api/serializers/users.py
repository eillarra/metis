from rest_framework import serializers

from epione.models.users import User


class UserMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
