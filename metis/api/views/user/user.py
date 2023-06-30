from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from metis.models import User
from ...permissions import IsAuthenticated
from ...serializers.user import AuthUserSerializer


class AuthUserViewSet(ViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthUserSerializer

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
