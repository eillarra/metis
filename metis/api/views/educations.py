from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from metis.models import Education, Student

from ..permissions import IsManager
from ..serializers import EducationSerializer, ProgramSerializer, StudentSerializer
from .base import BaseModelViewSet


class EducationViewSet(RetrieveModelMixin, GenericViewSet):
    """API endpoint for managing educations."""

    queryset = Education.objects.select_related("updated_by", "faculty")
    permission_classes = (IsManager,)
    serializer_class = EducationSerializer

    @method_decorator(never_cache)
    def retrieve(self, request, *args, **kwargs):
        """Return the education."""
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, pagination_class=None)
    @method_decorator(never_cache)
    def programs(self, request, *args, **kwargs):
        """Return all programs of the education."""
        programs = self.get_object().programs.prefetch_related("blocks__updated_by", "updated_by")
        return Response(ProgramSerializer(programs, many=True, context={"request": request}).data)

    @action(detail=True, pagination_class=None, url_path="student-users")
    @method_decorator(never_cache)
    def student_users(self, request, *args, **kwargs):
        """Return all student users of the education."""
        students = (
            Student.objects.filter(user=self.request.user, project__education=self.get_object())
            .prefetch_related("project__education", "block__internships")
            .distinct()
        )
        return Response(StudentSerializer(students, many=True, context={"request": request}).data)


class EducationNestedModelViewSet(BaseModelViewSet):
    """Base viewset for education child models."""

    _education = None

    def get_queryset(self):
        """Get queryset for education child models."""
        return super().get_queryset().filter(education=self.get_education())

    def get_education(self) -> "Education":
        """Get education object."""
        if not self._education:
            self._education = Education.objects.get(id=self.kwargs["parent_lookup_education_id"])
        return self._education

    def perform_create(self, serializer) -> None:
        """Create model instance."""
        self.validate(serializer)
        serializer.save(education=self.get_education(), created_by=self.request.user)

    def perform_update(self, serializer) -> None:
        """Update model instance."""
        self.validate(serializer)
        serializer.save(education=self.get_education(), updated_by=self.request.user)

    def validate(self, serializer) -> None:
        """Validate model instance."""
        try:
            Model = serializer.Meta.model
            Model(education=self.get_education(), **serializer.validated_data).clean()
        except Exception as exc:
            raise ValidationError(str(exc)) from exc
