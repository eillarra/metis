from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from metis.models import Project, User, Internship
from ...permissions import IsManager
from ...serializers.stages import InternshipSerializer, ProjectSerializer, PlaceSerializer, StudentSerializer


class ProjectViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Project.objects.select_related("updated_by", "education")
    permission_classes = (IsManager,)
    serializer_class = ProjectSerializer

    @action(detail=True, pagination_class=None)
    def internships(self, request, *args, **kwargs):
        internships = Internship.objects.filter(student__project=self.get_object()).prefetch_related(
            "program_internship__block", "track", "discipline"
        )
        return Response(InternshipSerializer(internships, many=True, context={"request": request}).data)

    @action(detail=True, pagination_class=None)
    def places(self, request, *args, **kwargs):
        places = self.get_object().places.prefetch_related(
            "institution__region", "contacts__user", "disciplines", "updated_by"
        )
        return Response(PlaceSerializer(places, many=True, context={"request": request}).data)

    @action(detail=True, pagination_class=None)
    def students(self, request, *args, **kwargs):
        students = (
            User.objects.filter(student_objects__project=self.get_object())
            .prefetch_related("student_objects__project", "student_objects__block")
            .distinct()
        )
        return Response(StudentSerializer(students, many=True, context={"request": request}).data)
