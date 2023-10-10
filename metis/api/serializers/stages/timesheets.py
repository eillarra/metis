from rest_framework import serializers

from metis.models.stages.timesheets import Absence, Timesheet
from ..base import BaseModelSerializer, NestedHyperlinkField
from ..rel.remarks import RemarksMixin


internship_lookup_fields = {
    "parent_lookup_education_id": "internship__project__education_id",
    "parent_lookup_project_id": "internship__project_id",
    "parent_lookup_internship_id": "internship_id",
}


class AbsenceSerializer(RemarksMixin, BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-internship-absence-detail", nested_lookup=internship_lookup_fields)
    internship = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Absence
        exclude = ("created_at", "created_by")


class TimesheetSerializer(BaseModelSerializer):
    self = NestedHyperlinkField("v1:project-internship-timesheet-detail", nested_lookup=internship_lookup_fields)
    internship = serializers.PrimaryKeyRelatedField(read_only=True)
    duration = serializers.TimeField(read_only=True)

    class Meta:
        model = Timesheet
        exclude = ("created_at", "created_by")
        read_only_fields = ("is_approved",)
