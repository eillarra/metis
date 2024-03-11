from rest_framework import serializers

from metis.models.emails import EmailLog

from .base import NestedHyperlinkField
from .stages.internships import InternshipSerializer


project_lookup_fields = {
    "parent_lookup_education_id": "project__education_id",
    "parent_lookup_project_id": "project_id",
}


class EmailTinySerializer(serializers.ModelSerializer):
    """Email tiny serializer."""

    self = NestedHyperlinkField("v1:project-email-detail", nested_lookup=project_lookup_fields)

    class Meta:  # noqa: D106
        model = EmailLog
        fields = ("id", "self", "sent_at", "subject", "to", "bcc", "reply_to", "tags")


class EmailSerializer(serializers.ModelSerializer):
    """Email serializer."""

    internship = InternshipSerializer(read_only=True)

    class Meta:  # noqa: D106
        model = EmailLog
        fields = "__all__"
