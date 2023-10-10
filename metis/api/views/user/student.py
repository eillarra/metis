from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from metis.models.rel.signatures import Signature
from metis.models.stages import Student
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
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        user_id = self.request.data["user"]

        if user_id != self.request.user.id:
            raise PermissionDenied("This student does not belong to this user")

        serializer.save(
            user=self.request.user,
            content_type_id=self.request.data["content_type"],
            object_id=self.request.data["object_id"],
        )

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
