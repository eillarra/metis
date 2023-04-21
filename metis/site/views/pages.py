from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from metis.api.serializers.faculties import EducationSerializer
from .inertia import InertiaView


class HomeView(InertiaView):
    vue_entry_point = "apps/home/main.ts"


class DashboardView(InertiaView):
    vue_entry_point = "apps/dashboard/main.ts"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_props(self, request, *args, **kwargs):
        return {
            "educations": EducationSerializer(request.user.educations, many=True, context={"request": request}).data,
        }
