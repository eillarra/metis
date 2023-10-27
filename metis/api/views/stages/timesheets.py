from http import HTTPStatus as status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from metis.models import Absence, Timesheet, Signature
from ...serializers import AbsenceSerializer, TimesheetSerializer
from .internships import InternshipNestedModelViewSet


class TimesheetPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        internship = view.get_internship()

        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated) and (
                internship.place.can_be_managed_by(request.user)
                or internship.student.user == request.user
                or internship.mentors.filter(user=request.user).exists()
            )

        if request.method == "POST" and request.resolver_match.url_name == "project-internship-timesheet-approve":
            return (
                internship.mentors.filter(user=request.user).exists()
                or internship.place.contacts.filter(user=request.user, is_admin=True).exists()
            )

        return internship.student.user == request.user

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.internship.student.user == request.user


class AbsenceViewSet(InternshipNestedModelViewSet):
    queryset = Absence.objects.prefetch_related("internship__project__education", "files")
    pagination_class = None
    permission_classes = (TimesheetPermissions,)
    serializer_class = AbsenceSerializer


class TimesheetViewSet(InternshipNestedModelViewSet):
    queryset = Timesheet.objects.prefetch_related("internship__project__education")
    pagination_class = None
    permission_classes = (TimesheetPermissions,)
    serializer_class = TimesheetSerializer

    @action(detail=False, methods=["post"])
    def approve(self, request, *args, **kwargs):
        internship = self.get_internship()
        timesheet_ids = request.data.get("ids", [])
        signed_text = request.data.get("signed_text", "")

        for timesheet in internship.timesheets.filter(id__in=timesheet_ids, is_approved=False):
            signature = Signature.objects.create(content_object=timesheet, user=request.user, signed_text=signed_text)
            Timesheet.approve(timesheet, signature)

        return Response(status=status.NO_CONTENT)
