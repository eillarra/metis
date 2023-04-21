from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .inertia import InertiaView


class HomeView(InertiaView):
    vue_entry_point = "apps/home/main.ts"


class DashboardView(InertiaView):
    vue_entry_point = "apps/dashboard/main.ts"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
