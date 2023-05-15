from ...serializers.rel.remarks import ContentSerializer
from .base import RelModelViewSet


class ContentViewSet(RelModelViewSet):
    auto_created_by = True
    pagination_class = None
    serializer_class = ContentSerializer

    def get_queryset(self):
        return self.get_content_object().contents.select_related("updated_by")
