from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from metis.models import User, TmpData
from ...permissions import IsAuthenticated
from ...serializers.user import AuthUserSerializer, AuthUserTmpDataSerializer


class AuthUserViewSet(ViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthUserSerializer

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class AuthUserTmpOasisViewSet(ViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthUserTmpDataSerializer

    def get_queryset(self):
        return TmpData.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().first()

    def create(self, request, *args, **kwargs):
        serializer = AuthUserTmpDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, created_by=request.user)
        return Response(AuthUserSerializer(request.user).data)

    def put(self, request, *args, **kwargs):
        serializer = AuthUserTmpDataSerializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, updated_by=request.user)
        return Response(AuthUserSerializer(request.user).data)

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.put(request, *args, **kwargs)
