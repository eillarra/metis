from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from metis.models import Absence, Timesheet
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
