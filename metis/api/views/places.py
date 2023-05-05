from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from metis.models.places import Place
from ..permissions import IsUser
from ..serializers import PlaceSerializer


class PlaceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Place.objects.select_related("updated_by", "region")
    permission_classes = (IsUser,)
    serializer_class = PlaceSerializer
