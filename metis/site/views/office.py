from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from metis.api.serializers.faculties import EducationSerializer
from metis.api.serializers.stages.projects import ProjectSerializer
from metis.models import Education
from .inertia import InertiaView


class OfficeView(InertiaView):
    vue_entry_point = "apps/office/main.ts"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().can_be_managed_by(request.user):
            messages.error(
                request,
                "You don't have the necessary permissions to access this page.",
            )
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Education:
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Education, code=self.kwargs.get("code"))
        return self.object

    def get_props(self, request, *args, **kwargs):
        projects = self.get_object().projects.prefetch_related("periods")

        return {
            "education": EducationSerializer(self.get_object(), context={"request": request}).data,
            "projects": ProjectSerializer(projects, many=True, context={"request": request}).data,
        }
