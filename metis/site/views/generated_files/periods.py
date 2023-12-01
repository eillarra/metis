from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest, PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.models import Period
from metis.services.file_generator.excel import PeriodIntershipsExcel


class PeriodFileView(View):
    """Generate an Excel file with all the internships of a period."""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().project.can_be_managed_by(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Period:
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Period, id=self.kwargs.get("period_id"))
        return self.object

    def get(self, request, *args, **kwargs):
        file_type = self.kwargs.get("file_type")

        if file_type == "xlsx":
            return PeriodIntershipsExcel(self.get_object()).get_response()
        else:
            raise BadRequest("Invalid file type")
