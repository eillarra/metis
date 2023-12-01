from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest, PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.models import Questioning
from metis.services.file_generator.pdf import render_pdf_template
from metis.services.file_generator.planner.planning import PlanningExcel
from metis.services.file_generator.questionings.base import QuestioningExcel


class QuestioningFileView(View):
    template_name = "pdfs/questioning.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().project.can_be_managed_by(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Questioning:
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Questioning, id=self.kwargs.get("questioning_id"))
        return self.object

    def get(self, request, *args, **kwargs):
        context = {"questioning": self.get_object()}
        file_type = self.kwargs.get("file_type")

        if file_type == "pdf":
            return render_pdf_template(request, self.template_name, context)
        elif file_type == "xlsx":
            return QuestioningExcel(self.get_object()).get_response()
        else:
            raise BadRequest("Invalid file type")


class PlanningFileView(QuestioningFileView):
    """Generate an Excel file with the planning for a tops questioning."""

    def get(self, request, *args, **kwargs):
        """Get response for the planning file."""
        if not self.get_object().type == Questioning.STUDENT_TOPS:
            raise BadRequest("Invalid questioning type")

        def int_list(s: str | None) -> list[int] | None:
            return [int(id) for id in s.split(",") if id] if s else None

        return PlanningExcel(
            self.get_object(),
            options={
                "students_with_first_choice": int_list(request.GET.get("s_first")),
                "students_to_skip": int_list(request.GET.get("s_skip")),
                "places_with_students": int_list(request.GET.get("p_force")),
                "places_to_skip": int_list(request.GET.get("p_skip")),
            },
        ).get_response()
