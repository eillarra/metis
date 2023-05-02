from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from metis.models import Project, Place, User
from ...permissions import IsManager
from ...serializers.places import PlaceSerializer
from ...serializers.stages import ProjectSerializer, StudentSerializer


class ProjectViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Project.objects.select_related("updated_by", "education")
    permission_classes = (IsManager,)
    serializer_class = ProjectSerializer

    @action(detail=True, pagination_class=None)
    def places(self, request, *args, **kwargs):
        places = (
            Place.objects.filter(project=self.get_object())
            .prefetch_related("region", "disciplines", "updated_by")
            .distinct()
        )
        return Response(PlaceSerializer(places, many=True, context={"request": request}).data)

    @action(detail=True, pagination_class=None)
    def students(self, request, *args, **kwargs):
        students = (
            User.objects.filter(student_records__project=self.get_object())
            .prefetch_related("student_records__project", "student_records__block")
            .distinct()
        )
        return Response(StudentSerializer(students, many=True, context={"request": request}).data)
