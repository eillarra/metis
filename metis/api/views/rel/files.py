import json

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

    def create(self, request, *args, **kwargs):
        """Convert tags to a valid JSON object. This is necessary because we get the multipart data mengled..."""
        json_data = json.loads(request.data.get("json", "{}"))
        request.data["description"] = json_data.get("description", "")
        request.data["tags"] = json.dumps(json_data.get("tags", []))
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Perform create action for related files."""
        serializer.save(content_object=self.get_content_object())
