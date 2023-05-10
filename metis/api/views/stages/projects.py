from rest_framework.decorators import action
from rest_framework.response import Response
from typing import TYPE_CHECKING

from metis.models import Project, User, Internship
from ...permissions import IsEducationOfficeMember
from ...serializers.stages import InternshipSerializer, ProjectSerializer, StudentSerializer
from ..base import BaseModelViewSet
from ..educations import EducationNestedModelViewSet

if TYPE_CHECKING:
    from metis.models import Education


class ProjectViewSet(EducationNestedModelViewSet):
    queryset = Project.objects.select_related("updated_by").prefetch_related("periods")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ProjectSerializer

    @action(detail=True, pagination_class=None)
    def internships(self, request, *args, **kwargs):
        internships = Internship.objects.filter(student__project=self.get_object()).prefetch_related(
            "program_internship__block", "track", "discipline"
        )
        return Response(InternshipSerializer(internships, many=True, context={"request": request}).data)

    @action(detail=True, pagination_class=None)
    def students(self, request, *args, **kwargs):
        students = (
            User.objects.filter(student_set__project=self.get_object())
            .prefetch_related("student_set__project", "student_set__block__internships")
            .distinct()
        )
        return Response(StudentSerializer(students, many=True, context={"request": request}).data)


class ProjectNestedModelViewSet(BaseModelViewSet):
    _project = None

    def get_queryset(self):
        return super().get_queryset().filter(project=self.get_project())

    def get_education(self) -> "Education":
        return self.get_project().education

    def get_project(self) -> "Project":
        if self._project:
            return self._project
        self._project = Project.objects.get(id=self.kwargs["parent_lookup_project_id"])
        return self._project

    def perform_create(self, serializer):
        serializer.save(project=self.get_project())
