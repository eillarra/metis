from django.contrib.contenttypes.models import ContentType
from rest_framework.viewsets import ModelViewSet

from ...permissions import IsRelManager


class RelModelViewSet(ModelViewSet):
    _content_object = None
    auto_created_by = False
    permission_classes = (IsRelManager,)

    def get_content_object(self):
        if self._content_object:
            return self._content_object

        # get ContentType content object based on the URL parameters
        content_type_id = self.kwargs.get("parent_lookup_content_type_id")
        object_id = self.kwargs.get("parent_lookup_object_id")
        self._content_object = ContentType.objects.get(id=content_type_id).get_object_for_this_type(id=object_id)
        return self._content_object

    def perform_create(self, serializer):
        if self.auto_created_by:
            serializer.save(content_object=self.get_content_object(), created_by=self.request.user)
        else:
            serializer.save(content_object=self.get_content_object())
