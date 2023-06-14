from rest_framework import serializers

from metis.models.stages.dates import ImportantDate
from ..base import BaseModelSerializer
from ..rel.forms import CustomFormSerializer


class ImportantDateSerializer(BaseModelSerializer):
    """
    TODO: this is currently read-only, but should be writable in the future.
    Updated via the admin interface for now.
    """

    form = CustomFormSerializer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = ImportantDate
        exclude = ("created_at", "created_by")
