from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.models import Project
from metis.services.file_generator.projects import ProjectContactsExcel, ProjectPlacesExcel, ProjectPlanningExcel


class ProjectExcelView(View):
    """Generate an Excel file for a project."""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Check if the user can access the project data."""
        if not self.get_object().can_be_managed_by(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Project:
        """Get the project."""
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Project, id=self.kwargs.get("project_id"))
        return self.object

    def get(self, request, *args, **kwargs):
        """Get a response with an Excel file."""
        code = self.kwargs.get("file_code")
        if code == "planning":
            return ProjectPlanningExcel(self.get_object()).get_response()
        elif code == "contacts":
            return ProjectContactsExcel(self.get_object()).get_response()
        elif code == "places":
            return ProjectPlacesExcel(self.get_object()).get_response()
        else:
            raise NotImplementedError
