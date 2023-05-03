from metis.models.disciplines import Discipline
from .base import BaseModelSerializer


class DisciplineSerializer(BaseModelSerializer):
    class Meta:
        model = Discipline
        fields = ("id", "code", "name", "color")
