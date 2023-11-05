from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from metis.models import User

from ..permissions import IsOfficeMember
from ..serializers import UserTinySerializer


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.order_by("first_name", "last_name")
    permission_classes = (IsOfficeMember,)
    serializer_class = UserTinySerializer

    filter_backends = (SearchFilter,)
    search_fields = ("username", "first_name", "last_name", "email", "emailaddress__email")
