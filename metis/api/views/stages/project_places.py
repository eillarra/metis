from rest_framework.filters import SearchFilter

from metis.models import ProjectPlace
from ...permissions import IsEducationOfficeMember
from ...serializers import ProjectPlaceSerializer
from .projects import ProjectNestedModelViewSet


class ProjectPlaceViewSet(ProjectNestedModelViewSet):
    queryset = ProjectPlace.objects.select_related("place").prefetch_related(
        "disciplines",
        "place__contacts__user",
        "place__contacts__updated_by",
        "place__region",
        "place__updated_by",
        "updated_by",
    )
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ProjectPlaceSerializer

    filter_backends = (SearchFilter,)
    search_fields = ("place__name", "place__code")
