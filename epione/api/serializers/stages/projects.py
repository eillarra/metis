from epione.models.stages.projects import Project
from ..base import BaseModelSerializer


class ProjectSerializer(BaseModelSerializer):

    class Meta:
        model = Project
        exclude = ("created_at", "created_by")
