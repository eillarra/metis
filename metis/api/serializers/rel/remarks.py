from rest_framework import serializers

from metis.models.rel.remarks import Remark
from ..users import UserTinySerializer
from .base import RelHyperlinkedField, NestedRelHyperlinkField


class RemarkSerializer(serializers.ModelSerializer):
    self = NestedRelHyperlinkField(view_name="v1:remark-detail")
    created_by = UserTinySerializer(read_only=True)

    class Meta:
        model = Remark
        fields = ("self", "text", "created_by", "created_at")


class RemarksMixin(serializers.ModelSerializer):
    rel_remarks = RelHyperlinkedField(view_name="v1:remark-list")
