from modeltranslation.fields import TranslationField
from rest_framework import serializers

from .users import UserBasicSerializer


class BaseModelSerializer(serializers.ModelSerializer):
    updated_by = UserBasicSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.model._meta.fields:
            if isinstance(field, TranslationField):
                self.fields.pop(field.name)
