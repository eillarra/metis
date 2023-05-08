from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from metis.models import Education, EducationPlace, User
from ..permissions import IsManager, IsEducationOfficeMember
from ..serializers import (
    EducationSerializer,
    EducationPlaceSerializer,
    ProgramSerializer,
    StudentSerializer,
)
from .base import BaseModelViewSet


class EducationViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Education.objects.select_related("updated_by", "faculty")
    permission_classes = (IsManager,)
    serializer_class = EducationSerializer

    @action(detail=True, pagination_class=None)
    def programs(self, request, *args, **kwargs):
        programs = self.get_object().programs.prefetch_related("blocks__updated_by", "updated_by")
        return Response(ProgramSerializer(programs, many=True, context={"request": request}).data)

    @action(detail=True, pagination_class=None)
    def students(self, request, *args, **kwargs):
        students = (
            User.objects.filter(student_set__project__education=self.get_object())
            .prefetch_related("student_set__project", "student_set__block__internships")
            .distinct()
        )
        return Response(StudentSerializer(students, many=True, context={"request": request}).data)


class EducationNestedModelViewSet(NestedViewSetMixin, BaseModelViewSet):
    _education = None

    def get_education(self):
        if self._education:
            return self._education
        self._education = Education.objects.get(id=self.kwargs["parent_lookup_education"])
        return self._education

    def perform_create(self, serializer):
        serializer.save(education=self.get_education())


class EducationPlaceViewSet(EducationNestedModelViewSet):
    queryset = EducationPlace.objects.prefetch_related("contacts__user", "place__region", "updated_by")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = EducationPlaceSerializer
