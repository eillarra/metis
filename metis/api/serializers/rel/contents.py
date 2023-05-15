from rest_framework import serializers

from metis.models.rel.contents import Content
from ..users import UserTinySerializer
from .base import RelHyperlinkedField, NestedRelHyperlinkField


class ContentSerializer(serializers.ModelSerializer):
    self = NestedRelHyperlinkField(view_name="v1:content-detail")
    updated_by = UserTinySerializer(read_only=True)

    class Meta:
        model = Content
        fields = ("id", "self", "text", "updated_at", "updated_by")


class ContentsMixin(serializers.ModelSerializer):
    rel_contents = RelHyperlinkedField(view_name="v1:content-list")
