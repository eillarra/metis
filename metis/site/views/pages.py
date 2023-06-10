from django import http
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import View

from metis.api.serializers import EducationTinySerializer, EducationSerializer, PlaceSerializer
from metis.models import Education, Place
from metis.models.rel.invitations import Invitation
from .inertia import InertiaView


class HomeView(InertiaView):
    vue_entry_point = "apps/home/main.ts"


class DashboardView(InertiaView):
    vue_entry_point = "apps/dashboard/main.ts"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_props(self, request, *args, **kwargs):
        data = {
            "educations": [],
            "places": [],
            "student_educations": [],
        }

        if request.user.is_office_member:
            data["educations"] = list(
                EducationSerializer(request.user.education_set, many=True, context={"request": request}).data
            )

        if request.user.is_contact:
            places = Place.objects.filter(contacts__user_id=request.user.id)
            data["places"] = list(PlaceSerializer(places, many=True, context={"request": request}).data)

        if request.user.is_student:
            educations = Education.objects.filter(projects__students__user_id=request.user.id).distinct()
            data["student_educations"] = list(
                EducationTinySerializer(educations, many=True, context={"request": request}).data
            )

        return data


class InvitationView(View):
    """
    Visiting this view processes an invitation and redirects the user to his/her dashboard.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, uuid: str, secret: str) -> http.HttpResponse:
        try:
            invitation = Invitation.objects.get(uuid=uuid)
        except Invitation.DoesNotExist:
            return http.HttpResponseNotFound("Invitation has expired")
        if invitation.secret != secret:
            return http.HttpResponseNotFound("Invitation does not exist")
        invitation.process(request.user)
        return http.HttpResponseRedirect(reverse("dashboard"))
