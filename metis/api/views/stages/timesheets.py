from http import HTTPStatus as status

from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response

from metis.models import Absence, Signature, Timesheet

from ...serializers import AbsenceSerializer, TimesheetSerializer
from .internships import InternshipNestedModelViewSet


class TimesheetPermissions(BasePermission):
    """Permissions for timesheets."""

    def has_permission(self, request, view):
        """Check if the user has permission to access the view."""
        if not bool(request.user and request.user.is_authenticated):
            return False

        internship = view.get_internship()

        if request.method in SAFE_METHODS:
            return (
                internship.place.can_be_managed_by(request.user)
                or internship.student.user == request.user
                or internship.mentors.filter(user=request.user).exists()
            )

        if request.method == "POST" and request.resolver_match.url_name == "project-internship-timesheet-approve":
            return internship.place.user_is_admin(request.user) or internship.mentors.filter(user=request.user).exists()

        return internship.student.user == request.user

    def has_object_permission(self, request, view, obj):
        """Check if the user has permission to manipulate the Timesheet object."""
        if request.method in SAFE_METHODS:
            return True

        return obj.internship.student.user == request.user


class AbsenceViewSet(InternshipNestedModelViewSet):
    """API endpoint for absences."""

    queryset = Absence.objects.prefetch_related("internship__project__education", "files")
    pagination_class = None
    permission_classes = (TimesheetPermissions,)
    serializer_class = AbsenceSerializer


class TimesheetViewSet(InternshipNestedModelViewSet):
    """API endpoint for timesheets."""

    queryset = Timesheet.objects.prefetch_related("internship__project__education")
    pagination_class = None
    permission_classes = (TimesheetPermissions,)
    serializer_class = TimesheetSerializer

    def perform_update(self, serializer) -> None:
        """Update model instance, reseting the approval status.

        Students can only update approved timesheets if they pass the "__reapprove" flag
        """
        if serializer.instance.is_approved and not self.request.data.get("__reapprove", False):
            raise PermissionDenied("Cannot update approved timesheet without reapproval request")
        else:
            self.request.data["is_approved"] = False
            self.request.data.pop("__reapprove", None)

        self.validate(serializer)
        serializer.save(internship=self.get_internship(), is_approved=False, updated_by=self.request.user)

    @action(detail=False, methods=["post"])
    def approve(self, request, *args, **kwargs):
        """Approve timesheet(s)."""
        internship = self.get_internship()
        timesheet_ids = request.data.get("ids", [])
        signed_text = request.data.get("signed_text", "")

        for timesheet in Timesheet.objects.filter(internship=internship, id__in=timesheet_ids, is_approved=False):
            signature = Signature.objects.create(content_object=timesheet, user=request.user, signed_text=signed_text)
            Timesheet.approve(timesheet, signature)

        return Response(status=status.NO_CONTENT)
