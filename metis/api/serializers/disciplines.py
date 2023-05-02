from rest_framework import serializers

from metis.models.disciplines import Discipline


class DisciplineTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ("id", "code", "name")
