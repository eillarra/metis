from metis.models.rel.forms import CustomFormResponse
from ...serializers.rel.forms import CustomFormResponseSerializer
from .base import RelModelViewSet


class CustomFormResponseViewSet(RelModelViewSet):
    auto_created_by = True
    pagination_class = None
    serializer_class = CustomFormResponseSerializer

    def get_queryset(self):
        return self.get_content_object().form_responses.select_related("updated_by")
