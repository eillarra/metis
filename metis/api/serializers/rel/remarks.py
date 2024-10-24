from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from rest_framework import serializers

from metis.models.rel.remarks import Remark

from ..base import TagsMixin
from ..users import UserTinySerializer
from .base import NestedRelHyperlinkField, RelHyperlinkedField


class RemarkSerializer(TagsMixin, serializers.ModelSerializer):
    """Remark serializer."""

    self = NestedRelHyperlinkField(view_name="v1:remark-detail")
    updated_by = UserTinySerializer(read_only=True)

    class Meta:  # noqa: D106
        model = Remark
        fields = ("id", "self", "text", "tags", "updated_at", "updated_by")


class RemarksMixin(serializers.ModelSerializer):
    """Remarks mixin."""

    rel_remarks = RelHyperlinkedField(view_name="v1:remark-list")
    remark_count = serializers.SerializerMethodField()

    _counts = {}

    def _get_counts(self, obj):
        """Get remark counts for all objects of a given ContentType, once per request.

        For performance reasons, we don't want to count remarks per object,
        so we do one query for the ContentType, and then use that with the object_id.
        """
        ct = ContentType.objects.get_for_model(obj)

        if ct.id not in self._counts:
            self._counts[ct.id] = (
                Remark.objects.filter(
                    content_type_id=ct.id,
                )
                .values("object_id")
                .annotate(Count("object_id"))
            )

        return self._counts[ct.id]

    def get_remark_count(self, obj):
        """Get remark count for a given object."""
        match = next((i for i in self._get_counts(obj) if i["object_id"] == obj.id), None)
        return match["object_id__count"] if match else 0
