from metis.models.disciplines import Discipline

from .base import BaseTranslatedModelSerializer


class DisciplineSerializer(BaseTranslatedModelSerializer):
    class Meta:
        model = Discipline
        fields = ("id", "code", "name", "color")
