from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from metis.models.places import Place
from ..permissions import IsAuthenticated
from ..serializers import PlaceSerializer


class PlaceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Place.objects.select_related("region", "updated_by")
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaceSerializer
