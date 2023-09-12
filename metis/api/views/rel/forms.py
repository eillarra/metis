from rest_framework import serializers

from ...serializers.rel.forms import FormResponseSerializer
from .base import RelModelViewSet


class CustomFormResponseViewSet(RelModelViewSet):
    auto_created_by = True
    pagination_class = None
    serializer_class = FormResponseSerializer

    def get_queryset(self):
        return self.get_content_object().form_responses.select_related("updated_by")  # type: ignore

    def perform_create(self, serializer):
        self.validate_form_response(serializer)
        super().perform_create(serializer)

    def perform_update(self, serializer):
        self.validate_form_response(serializer)
        super().perform_update(serializer)

    def validate_form_response(self, serializer) -> None:
        try:
            serializer.validated_data["questioning"].clean_response_data(serializer.validated_data["data"])
        except ValueError as e:
            raise serializers.ValidationError({"data": str(e)})
