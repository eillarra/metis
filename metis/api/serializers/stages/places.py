from metis.models.stages.places import ProjectPlace
from ..base import BaseModelSerializer
from ..disciplines import DisciplineSerializer
from ..places import PlaceSerializer


class ProjectPlaceSerializer(BaseModelSerializer):
    place = PlaceSerializer()
    disciplines = DisciplineSerializer(many=True)

    class Meta:
        model = ProjectPlace
        exclude = ("created_at", "created_by")
