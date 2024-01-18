from http import HTTPStatus as status
from typing import TYPE_CHECKING

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from metis.models import Project, Student, User

from ...permissions import IsEducationOfficeMember
from ...serializers.stages import ProjectSerializer, StudentUserSerializer
from ...serializers.stages.students import StudentSerializer
from ..base import BaseModelViewSet
from ..educations import EducationNestedModelViewSet


if TYPE_CHECKING:
    from metis.models import Education


class ProjectViewSet(EducationNestedModelViewSet):
    """API endpoint for managing projects."""

    queryset = Project.objects.select_related("updated_by").prefetch_related(
        "periods__updated_by", "questionings__updated_by"
    )
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["post"])
    def invite(self, request, *args, **kwargs):
        """Invite student to project."""
        emails = request.data.get("emails")
        data = request.data.get("data", {})

        if not emails:
            return Response({"emails": ["Must provide emails"]}, status=status.BAD_REQUEST)

        user = User.create_from_name_emails(name=request.data.get("name"), emails=emails)
        student = Student.objects.create(project=self.get_object(), user=user, created_by=self.request.user, **data)
        self.get_object().students.add(student)

        return Response(StudentSerializer(student, context={"request": request}).data, status=status.CREATED)

    @action(detail=True, pagination_class=None, url_path="student-users")
    @method_decorator(never_cache)
    def student_users(self, request, *args, **kwargs):
        """Return all student users of the project."""
        students = (
            User.objects.filter(student_set__project=self.get_object())
            .prefetch_related(
                "student_set__project__education", "student_set__block__internships", "student_set__updated_by"
            )
            .distinct()
        )
        return Response(StudentUserSerializer(students, many=True, context={"request": request}).data)


class ProjectNestedModelViewSet(BaseModelViewSet):
    """Base viewset for project child models."""

    _project = None

    def get_queryset(self):
        """Get queryset for project child models."""
        return super().get_queryset().filter(project=self.get_project())

    def get_education(self) -> "Education":
        """Get education from project object."""
        return self.get_project().education

    def get_project(self) -> "Project":
        """Get project object."""
        if not self._project:
            self._project = Project.objects.get(id=self.kwargs["parent_lookup_project_id"])
        return self._project

    def perform_create(self, serializer) -> None:
        """Create model instance."""
        self.validate(serializer)
        serializer.save(project=self.get_project(), created_by=self.request.user)

    def perform_update(self, serializer) -> None:
        """Update model instance."""
        self.validate(serializer)
        serializer.save(project=self.get_project(), updated_by=self.request.user)

    def validate(self, serializer) -> None:
        """Validate model instance."""
        try:
            Model = serializer.Meta.model
            Model(project=self.get_project(), **serializer.validated_data).clean()
        except Exception as exc:
            raise ValidationError(str(exc)) from exc
