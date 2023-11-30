from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.api.serializers import (
    AuthStudentSerializer,
    EducationTinySerializer,
    FileSerializer,
    InternshipFullInertiaSerializer,
    ProjectSerializer,
)
from metis.models import Education, Internship
from metis.services.reporter.pdf import ProjectPlaceInformationPdf

from .inertia import InertiaView
from .reports.periods import PeriodReportMixin


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
        projects = self.get_education().projects.filter(students__user=request.user)
        last_project = projects.get(name="AJ23-24")  # TODO: clean

        base = {
            "education": EducationTinySerializer(self.get_education()).data,
            "files": FileSerializer(last_project.files.all(), many=True, context={"request": request}).data,
            "projects": ProjectSerializer(projects, many=True, context={"request": request}).data,
            "student_set": AuthStudentSerializer(
                self.get_student_set(request.user), many=True, context={"request": request}
            ).data,
            "internships": InternshipFullInertiaSerializer(
                Internship.objects.filter(
                    student__user=request.user, project=last_project, status=Internship.DEFINITIVE
                ),
                many=True,
                context={"request": request},
            ).data,
        }

        # --------------
        # PROVISIONAL
        # --------------
        from metis.api.serializers import AuthUserSerializer, ProjectTinySerializer, TextEntrySerializer
        from metis.models import Project

        try:
            project = Project.objects.get(education=self.get_education(), name="AJ22-23")
            place_ids = list(
                Internship.objects.filter(student__in=self.get_student_set(request.user)).values_list(
                    "project_place__place_id", flat=True
                )
            )
            discipline_ids = list(
                Internship.objects.filter(student__in=self.get_student_set(request.user)).values_list(
                    "discipline_id", flat=True
                )
            )
        except Exception:
            place_ids = None
            discipline_ids = None

        period_id = 11 if self.get_education().code == "audio" else 20
        project = Project.objects.get(education=self.get_education(), name="AJ23-24")

        temp_props = {
            "academic_year": project.academic_year,
            "project": ProjectTinySerializer(project).data,
            "user": AuthUserSerializer(request.user, context={"request": request}).data,
            "student": AuthStudentSerializer(
                self.get_student_set(request.user).get(project=project), context={"request": request}
            ).data,
            "required_texts": TextEntrySerializer(project.required_texts, many=True, context={"request": request}).data,
            "project_place_options": [
                {
                    "place_id": project_place.place_id,
                    "value": project_place.id,
                    "label": project_place.place.name,
                    "disciplines": " ".join(project_place.disciplines.values_list("name", flat=True)) or "",
                }
                for project_place in project.place_set.filter(
                    availability_set__period_id=period_id, availability_set__min__gt=0
                ).order_by("place__name")
            ],
            "place_ids": place_ids,
            "discipline_ids": discipline_ids,
        }
        # --------------
        # --------------

        return {**base, **temp_props}

    def get_page_title(self, request, *args, **kwargs) -> str:
        return f"{self.get_education().short_name} - Stages"


class StudentAreaPeriodReportView(StudentAreaFirewallMixin, PeriodReportMixin, View):
    available_reports = {"pdf": {"project_place_information": ProjectPlaceInformationPdf}}

    def get(self, request, *args, **kwargs):
        period = self.get_period()

        if not self.get_student_set(request.user).filter(block=period.program_internship.block).exists():
            raise PermissionDenied

        return super().get(request, *args, **kwargs)
