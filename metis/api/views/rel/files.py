from rest_framework.parsers import MultiPartParser

from ...permissions import IsSharedRelManager
from ...serializers.rel.files import FileSerializer
from .base import RelModelViewSet


class FileViewSet(RelModelViewSet):
    """API endpoint for managing related files."""

    pagination_class = None
    parser_classes = [MultiPartParser]
    permission_classes = (IsSharedRelManager,)
    serializer_class = FileSerializer

    def get_queryset(self):
        """Get queryset for related files."""
        return self.get_content_object().files  # type: ignore

    def perform_create(self, serializer):
        """Perform create action for related files."""
        print(serializer.validated_data["file"].name)
        serializer.save(content_object=self.get_content_object())
