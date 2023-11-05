from rest_framework import serializers

from metis.models.rel.texts import TextEntry

from ..users import UserTinySerializer
from .base import NestedRelHyperlinkField, RelHyperlinkedField


class TextEntrySerializer(serializers.ModelSerializer):
    self = NestedRelHyperlinkField(view_name="v1:text-detail")
    updated_by = UserTinySerializer(read_only=True)
    title_en = serializers.CharField()
    title_nl = serializers.CharField()
    text_en = serializers.CharField()
    text_nl = serializers.CharField()
    version = serializers.IntegerField(read_only=True)

    class Meta:
        model = TextEntry
        fields = (
            "id",
            "self",
            "code",
            "version",
            "title_en",
            "title_nl",
            "text_en",
            "text_nl",
            "updated_at",
            "updated_by",
        )


class TextEntriesMixin(serializers.ModelSerializer):
    rel_texts = RelHyperlinkedField(view_name="v1:text-list")
