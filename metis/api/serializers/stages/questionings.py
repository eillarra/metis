from rest_framework import serializers

from metis.models.stages.questionings import Questioning
from ..base import BaseModelSerializer


class QuestioningSerializer(BaseModelSerializer):
    """
    TODO: this is currently read-only, but should be writable in the future.
    Updated via the admin interface for now.
    """

    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Questioning
        exclude = ("created_at", "created_by")
