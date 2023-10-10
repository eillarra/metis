from rest_framework import serializers

from metis.models.stages.questionings import Questioning
from ..base import BaseModelSerializer, NestedHyperlinkField


project_lookup_fields = {
    "parent_lookup_education_id": "project__education_id",
    "parent_lookup_project_id": "project_id",
}


class QuestioningTinySerializer(BaseModelSerializer):
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Questioning
        exclude = ("email_subject", "email_body", "email_add_office_in_bcc", "created_at", "created_by")


class QuestioningSerializer(QuestioningTinySerializer):
    self = NestedHyperlinkField("v1:project-questioning-detail", nested_lookup=project_lookup_fields)
    rel_responses = NestedHyperlinkField("v1:project-questioning-responses", nested_lookup=project_lookup_fields)
    target_object_ids = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = Questioning
        exclude = ()

    def get_target_object_ids(self, instance) -> list:
        return instance.get_target_group().values_list("id", flat=True)

    def get_stats(self, instance):
        return {
            "response_rate": round(min(100, instance.response_rate * 100), 1),
        }
