from metis.models import Internship
from ...permissions import IsEducationOfficeMember
from ...serializers import InternshipSerializer
from .projects import ProjectNestedModelViewSet


class InternshipViewSet(ProjectNestedModelViewSet):
    queryset = Internship.objects.prefetch_related("project__education", "period", "track", "discipline", "updated_by")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = InternshipSerializer
