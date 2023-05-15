from metis.models import Internship
from ...permissions import IsEducationOfficeMember
from ...serializers import InternshipSerializer
from .projects import ProjectNestedModelViewSet


class InternshipViewSet(ProjectNestedModelViewSet):
    queryset = Internship.objects.prefetch_related("period__project__education", "track", "discipline", "updated_by")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = InternshipSerializer

    def get_queryset(self):
        return self.queryset.filter(period__project=self.get_project())  # type: ignore
