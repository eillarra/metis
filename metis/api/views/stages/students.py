from metis.models import Student

from ...permissions import IsEducationOfficeMember
from ...serializers import StudentSerializer
from .projects import ProjectNestedModelViewSet


class StudentViewSet(ProjectNestedModelViewSet):
    """API endpoint for managing students."""

    queryset = Student.objects.select_related("project", "user").prefetch_related(
        "block__internships", "updated_by", "user__socialaccount_set"
    )
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = StudentSerializer
