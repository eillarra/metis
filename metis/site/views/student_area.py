from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.api.serializers import EducationTinySerializer, ProjectSerializer, AuthStudentSerializer
from metis.models import Education, Period
from metis.services.reporter.pdf import ProjectPlaceInformationReport
from .inertia import InertiaView


class StudentAreaFirewallMixin(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        student_set = self.get_student_set(request.user)

        if not student_set.filter(project__education=self.get_education()).exists():  # type: ignore
            messages.error(
                request,
                "You don't have the necessary permissions to access this page.",
            )
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_education(self) -> Education:
        if not hasattr(self, "education"):
            self.education = get_object_or_404(Education, code=self.kwargs.get("education_code"))
        return self.education

    def get_student_set(self, user):
        if not hasattr(self, "student_set"):
            self.student_set = user.student_set.filter(project__education=self.get_education())
        return self.student_set


class StudentAreaView(StudentAreaFirewallMixin, InertiaView):
    vue_entry_point = "apps/studentArea/main.ts"

    def get_props(self, request, *args, **kwargs):
        base = {
            "education": EducationTinySerializer(self.get_education()).data,
            "student_set": AuthStudentSerializer(
                self.get_student_set(request.user), many=True, context={"request": request}
            ).data,
        }

        # --------------
        # PROVISIONAL
        # --------------
        from metis.api.serializers import AuthUserSerializer, ProjectTinySerializer, TextEntrySerializer
        from metis.models import Project

        project = Project.objects.get(education=self.get_education(), name="AJ23-24")
        temp_props = {
            "academic_year": project.academic_year,
            "project": ProjectTinySerializer(project).data,
            "user": AuthUserSerializer(request.user).data,
            "student": AuthStudentSerializer(self.get_student_set(request.user).get(project=project)).data,
            "required_texts": TextEntrySerializer(project.required_texts, many=True, context={"request": request}).data,
        }
        # --------------
        # --------------

        return {**base, **temp_props}

    def get_page_title(self, request, *args, **kwargs) -> str:
        return f"{self.get_education().short_name} - Stages"


class StudentAreaPeriodPdfReportView(StudentAreaFirewallMixin, View):
    available_reports = {
        "project_place_information": ProjectPlaceInformationReport
    }

    def get(self, request, *args, **kwargs):
        period_id = kwargs.get("period_id")

        try:
            period = Period.objects.get(id=period_id, project__education=self.get_education())
        except Period.DoesNotExist:
            raise PermissionDenied

        if not self.get_student_set(request.user).filter(block=period.program_internship.block).exists():
            raise PermissionDenied

        try:
            report = self.available_reports[kwargs.get("code")](period_id)
        except KeyError:
            raise PermissionDenied

        return report.get_response()
