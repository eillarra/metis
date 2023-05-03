from metis.models.disciplines import Discipline
from .base import BaseModelSerializer


class DisciplineTinySerializer(BaseModelSerializer):
    class Meta:
        model = Discipline
        fields = ("code", "name")
