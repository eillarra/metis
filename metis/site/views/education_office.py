from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.api.serializers import EducationSerializer, EducationTinySerializer, ProgramSerializer, ProjectSerializer
from metis.models import Education, Period
from metis.services.reporter.pdf import ProjectPlaceInformationReport
from .inertia import InertiaView


class EducationOfficeFirewallMixin(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.get_education().can_be_managed_by(request.user):
            messages.error(
                request,
                "You don't have the necessary permissions to access this page.",
            )
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_education(self) -> Education:
        if not hasattr(self, "education"):
            queryset = Education.objects.all().prefetch_related("programs__blocks", "projects__periods")
            self.education = get_object_or_404(queryset, code=self.kwargs.get("education_code"))
        return self.education


class EducationOfficeView(EducationOfficeFirewallMixin, InertiaView):
    vue_entry_point = "apps/educationOffice/main.ts"

    def get_props(self, request, *args, **kwargs):
        programs = self.get_education().programs.prefetch_related("blocks")
        projects = self.get_education().projects.prefetch_related("periods")

        return {
            "education": EducationSerializer(self.get_education(), context={"request": request}).data,
            "educations": (
                EducationTinySerializer(request.user.education_set, many=True, context={"request": request}).data
            ),
            "programs": ProgramSerializer(programs, many=True, context={"request": request}).data,
            "projects": ProjectSerializer(projects, many=True, context={"request": request}).data,
        }

    def get_page_title(self, request, *args, **kwargs) -> str:
        return f"{self.get_education().short_name} - Stagebureau"


class EducationOfficePeriodPdfReportView(EducationOfficeFirewallMixin, View):
    available_reports = {
        "project_place_information": ProjectPlaceInformationReport
    }

    def get(self, request, *args, **kwargs):
        period_id = kwargs.get("period_id")

        try:
            Period.objects.get(id=period_id, project__education=self.get_education())
        except Period.DoesNotExist:
            raise PermissionDenied

        try:
            report = self.available_reports[kwargs.get("code")](period_id)
        except KeyError:
            raise PermissionDenied

        return report.get_response()
