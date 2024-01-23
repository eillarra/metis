from ...permissions import IsSharedRelManager
from ...serializers.rel.addresses import AddressSerializer
from .base import RelModelViewSet


class AddressViewSet(RelModelViewSet):
    """API endpoint for addresses."""

    pagination_class = None
    permission_classes = (IsSharedRelManager,)
    serializer_class = AddressSerializer

    def get_queryset(self):
        """Get queryset for addresses."""
        return self.get_content_object().addresses  # type: ignore
