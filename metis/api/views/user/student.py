from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from metis.models.stages import Student, Signature
from ...permissions import IsAuthenticated
from ...serializers import AuthStudentSerializer, AuthSignatureSerializer


class AuthStudentViewSet(ListModelMixin, GenericViewSet):
    queryset = Student.objects.all()
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthStudentSerializer

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AuthStudentSignatureViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Signature.objects.all()
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthSignatureSerializer

    def get_queryset(self):
        return super().get_queryset().filter(student__user=self.request.user)

    def perform_create(self, serializer):
        student_id: int = self.request.data["student"]
        student = Student.objects.get(id=student_id)
        if student.user != self.request.user:
            raise PermissionDenied("This student does not belong to this user")

        serializer.save(student_id=student_id)

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
