from rest_framework import serializers

from metis.models.stages.evaluations import Evaluation, EvaluationForm

from ..base import BaseModelSerializer, NestedHyperlinkField
from ..rel.remarks import RemarksMixin


internship_lookup_fields = {
    "parent_lookup_education_id": "internship__project__education_id",
    "parent_lookup_project_id": "internship__project_id",
    "parent_lookup_internship_id": "internship_id",
}


class EvaluationFormSerializer(BaseModelSerializer):
    """Evaluation form serializer."""

    definition = serializers.JSONField(read_only=True)

    class Meta:  # noqa: D106
        model = EvaluationForm
        exclude = ("form_definition", "created_at", "created_by")


class EvaluationSerializer(RemarksMixin, BaseModelSerializer):
    """Evaluation serializer."""

    self = NestedHyperlinkField("v1:project-internship-evaluation-detail", nested_lookup=internship_lookup_fields)
    uuid = serializers.UUIDField(read_only=True)
    internship = serializers.PrimaryKeyRelatedField(read_only=True)
    url = serializers.CharField(read_only=True, source="get_absolute_url")
    name = serializers.CharField(read_only=True)
    form_definition = serializers.JSONField(read_only=True, source="form.definition")
    evaluation_periods = serializers.JSONField(read_only=True)

    class Meta:  # noqa: D106
        model = Evaluation
        exclude = ("created_at", "created_by")
        read_only_fields = ("is_approved",)
