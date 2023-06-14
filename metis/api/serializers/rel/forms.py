from rest_framework import serializers

from metis.models.rel.forms import CustomForm, CustomFormResponse
from ..users import UserTinySerializer
from .base import RelHyperlinkedField, NestedRelHyperlinkField


class CustomFormSerializer(serializers.ModelSerializer):
    """
    TODO: this is currently read-only, but should be writable in the future.
    Updated via the admin interface for now.
    """

    class Meta:
        model = CustomForm
        exclude = ()


class CustomFormResponseSerializer(serializers.ModelSerializer):
    self = NestedRelHyperlinkField(view_name="v1:form-response-detail")
    updated_by = UserTinySerializer(read_only=True)

    class Meta:
        model = CustomFormResponse
        fields = (
            "id",
            "self",
            "data",
            "form",
            "updated_at",
            "updated_by",
        )


class CustomFormResponsesMixin(serializers.ModelSerializer):
    rel_form_responses = RelHyperlinkedField(view_name="v1:form-response-list")
