from ...permissions import IsSharedRelManager
from ...serializers.rel.texts import TextEntrySerializer
from .base import RelModelViewSet


class TextEntryViewSet(RelModelViewSet):
    auto_created_by = True
    pagination_class = None
    permission_classes = (IsSharedRelManager,)
    serializer_class = TextEntrySerializer

    def get_queryset(self):
        return self.get_content_object().texts.select_related("updated_by")  # type: ignore
