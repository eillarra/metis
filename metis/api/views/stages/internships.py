from http import HTTPStatus as status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from metis.models import User, Internship, Mentor, Project, Education
from ...permissions import IsEducationOfficeMember
from ...serializers import InternshipSerializer, MentorTinySerializer
from ..base import BaseModelViewSet
from .projects import ProjectNestedModelViewSet


class CanManageMentors(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.place.can_be_managed_by(request.user)


class InternshipViewSet(ProjectNestedModelViewSet):
    queryset = Internship.objects.prefetch_related("project__education", "period", "track", "discipline", "updated_by")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = InternshipSerializer

    def _check_user_id(self, request) -> int:
        user_id = request.data.get("user_id", None)

        if not user_id or not User.objects.filter(id=user_id).exists():
            raise ValidationError({"user_id": "No valid user id provided."})

        return user_id

    @action(detail=True, methods=["post"], permission_classes=(CanManageMentors,))
    def add_mentor(self, request, *args, **kwargs):
        user_id = self._check_user_id(request)
        mentor = Mentor.objects.create(internship=self.get_object(), user_id=user_id, created_by=request.user)
        serializer = MentorTinySerializer(mentor)
        return Response(serializer.data, status=status.CREATED, headers=self.get_success_headers(serializer.data))

    @action(detail=True, methods=["post"], permission_classes=(CanManageMentors,))
    def remove_mentor(self, request, *args, **kwargs):
        user_id = self._check_user_id(request)
        mentor = Mentor.objects.get(internship=self.get_object(), user_id=user_id)
        mentor.delete()
        return Response(status=status.NO_CONTENT)


class InternshipNestedModelViewSet(BaseModelViewSet):
    _internship = None

    def get_queryset(self):
        return super().get_queryset().filter(internship=self.get_internship())

    def get_education(self) -> "Education":
        return self.get_project().education

    def get_project(self) -> "Project":
        return self.get_internship().project

    def get_internship(self) -> "Internship":
        if not self._internship:
            self._internship = Internship.objects.get(id=self.kwargs["parent_lookup_internship_id"])
        return self._internship

    def perform_create(self, serializer):
        self.validate(serializer)
        serializer.save(internship=self.get_internship(), created_by=self.request.user)

    def perform_update(self, serializer):
        self.validate(serializer)
        serializer.save(internship=self.get_internship(), updated_by=self.request.user)

    def validate(self, serializer) -> None:
        try:
            ModelClass = serializer.Meta.model
            ModelClass(internship=self.get_internship(), **serializer.validated_data).clean()
        except Exception as e:
            raise ValidationError(str(e))
