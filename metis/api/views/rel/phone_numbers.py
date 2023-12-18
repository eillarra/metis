from ...permissions import IsSharedRelManager
from ...serializers.rel.phone_numbers import PhoneNumberSerializer
from .base import RelModelViewSet


class PhoneNumberViewSet(RelModelViewSet):
    """API endpoint for phone numbers."""

    pagination_class = None
    permission_classes = (IsSharedRelManager,)
    serializer_class = PhoneNumberSerializer

    def get_queryset(self):
        """Get queryset for phone numbers."""
        return self.get_content_object().phone_numbers  # type: ignore
