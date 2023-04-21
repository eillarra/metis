from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from metis.models import Education
from ..permissions import IsManager
from ..serializers import EducationSerializer, ProjectSerializer


class EducationViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Education.objects.select_related("updated_by", "faculty")
    permission_classes = (IsManager,)
    serializer_class = EducationSerializer

    @action(detail=True, pagination_class=None)
    def projects(self, request, *args, **kwargs):
        return Response(ProjectSerializer(self.get_object().projects, many=True).data)
