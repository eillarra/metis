from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest, PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.models import Questioning
from metis.services.file_generator.excel import QuestioningExcel
from metis.services.file_generator.pdf import render_pdf_template


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
