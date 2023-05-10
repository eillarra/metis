from metis.models import ProjectPlace
from ...permissions import IsEducationOfficeMember
from ...serializers import ProjectPlaceSerializer
from .projects import ProjectNestedModelViewSet


class ProjectPlaceViewSet(ProjectNestedModelViewSet):
    queryset = ProjectPlace.objects.select_related("education_place__place__region", "updated_by").prefetch_related(
        "disciplines"
    )
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ProjectPlaceSerializer
