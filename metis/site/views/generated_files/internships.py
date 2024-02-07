from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.models.stages.internships import Internship
from metis.services.file_generator.pdf import render_pdf_template


class InternshipPdfBaseView(View):
    """Internship PDF view."""

    template_name = "pdfs/internship.html"

    def get_object(self, queryset=None) -> Internship:
        """Get the internship."""
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Internship, uuid=self.kwargs.get("uuid"))
        return self.object

    def get_template_name(self) -> str:
        """Get the template name."""
        code = self.kwargs.get("template_code")
        return f"pdfs/internship_{code}.html"

    def get(self, request, *args, **kwargs):
        """Get a response with an PDF file for the internship."""
        context = {"internship": self.get_object()}
        return render_pdf_template(request, self.get_template_name(), context)


class InternshipPdfView(InternshipPdfBaseView):
    """Internship PDF view."""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if not self.get_object().can_be_viewed_by(request.user):
            messages.error(request, "You don't have access to this document.")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class InternshipPdfSecretView(InternshipPdfBaseView):
    """Internship PDF view, accessed using a secret link."""

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if self.get_object().secret != kwargs.get("secret"):
            messages.error(request, "You don't have access to this document.")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
