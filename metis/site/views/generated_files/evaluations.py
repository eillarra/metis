from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.models.stages.evaluations import Evaluation
from metis.services.file_generator.pdf import render_pdf_template


class EvaluationPdfView(View):
    template_name = "pdfs/evaluation.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().can_be_viewed_by(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Evaluation:
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Evaluation, uuid=self.kwargs.get("uuid"))
        return self.object

    def get(self, request, *args, **kwargs):
        context = {"evaluations": [self.get_object()]}
        return render_pdf_template(request, self.template_name, context)
