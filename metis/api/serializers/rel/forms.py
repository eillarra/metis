from rest_framework import serializers

from metis.models.rel.forms import FormResponse

from ..users import UserTinySerializer
from .base import NestedRelHyperlinkField, RelHyperlinkedField


class FormResponseSerializer(serializers.ModelSerializer):
    self = NestedRelHyperlinkField(view_name="v1:form-response-detail")
    updated_by = UserTinySerializer(read_only=True)
    object_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = FormResponse
        fields = (
            "id",
            "self",
            "data",
            "object_id",
            "questioning",
            "updated_at",
            "updated_by",
        )


class FormResponsesMixin(serializers.ModelSerializer):
    rel_form_responses = RelHyperlinkedField(view_name="v1:form-response-list")
