from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from metis.models import Education, User
from ..permissions import IsManager
from ..serializers import EducationSerializer, ProgramSerializer, ProjectSerializer, StudentSerializer


class EducationViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Education.objects.select_related("updated_by", "faculty")
    permission_classes = (IsManager,)
    serializer_class = EducationSerializer

    @action(detail=True, pagination_class=None)
    def projects(self, request, *args, **kwargs):
        projects = self.get_object().projects.prefetch_related("periods", "updated_by").distinct()
        return Response(ProjectSerializer(projects, many=True, context={"request": request}).data)

    @action(detail=True, pagination_class=None)
    def programs(self, request, *args, **kwargs):
        programs = self.get_object().programs.prefetch_related("blocks__updated_by", "updated_by").distinct()
        return Response(ProgramSerializer(programs, many=True, context={"request": request}).data)

    @action(detail=True, pagination_class=None)
    def students(self, request, *args, **kwargs):
        students = (
            User.objects.filter(student_records__project__education=self.get_object())
            .prefetch_related("student_records__project", "student_records__block")
            .distinct()
        )
        return Response(StudentSerializer(students, many=True, context={"request": request}).data)
