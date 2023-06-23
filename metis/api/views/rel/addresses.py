from ...permissions import IsSharedRelManager
from ...serializers.rel.addresses import AddressSerializer
from .base import RelModelViewSet


class AddressViewSet(RelModelViewSet):
    pagination_class = None
    permission_classes = (IsSharedRelManager,)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.get_content_object().addresses  # type: ignore
