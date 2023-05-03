from modeltranslation.fields import TranslationField
from rest_framework import serializers

from .users import UserTinySerializer


class BaseModelSerializer(serializers.ModelSerializer):
    updated_by = UserTinySerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.model._meta.fields:
            if isinstance(field, TranslationField):
                try:
                    self.fields.pop(field.name)
                except KeyError:
                    pass
