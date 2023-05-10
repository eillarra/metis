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


class NestedHyperlinkField(serializers.HyperlinkedIdentityField):
    """
    A field that returns the absolute URL to an API endpoint.
    Normally we should use HyperlinkedIdentityField, but it doesn't support
    nested routes. In this case we pass the view name and the kwargs to
    have an absolute URL calculated.
    """

    def __init__(self, view_name: str, nested_lookup: dict, *args, **kwargs):
        self.nested_lookup = nested_lookup
        kwargs["read_only"] = True
        super().__init__(view_name=view_name, *args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, "pk") and obj.pk in (None, ""):  # pragma: no cover
            return None

        extra_values = {}

        for key, value in self.nested_lookup.items():
            # get the object attribute respecting "__" as separator
            current_obj = obj
            for attr in value.split("__"):
                current_obj = getattr(current_obj, attr)
            extra_values[key] = current_obj

        if view_name.endswith("-list"):
            kwargs = extra_values
        else:
            kwargs = {self.lookup_url_kwarg: getattr(obj, self.lookup_field)} | extra_values

        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
