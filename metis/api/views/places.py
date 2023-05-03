from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from metis.models.institutions import Institution
from ..permissions import IsUser
from ..serializers import InstitutionSerializer


class InstitutionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Institution.objects.select_related("updated_by", "region")
    permission_classes = (IsUser,)
    serializer_class = InstitutionSerializer
