from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from metis.api.serializers import EducationTinySerializer, PlaceSerializer
from metis.models import Place
from .inertia import InertiaView


class PlaceOfficeView(InertiaView):
    vue_entry_point = "apps/placeOffice/main.ts"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().contacts.filter(user=request.user).exists():
            messages.error(
                request,
                "You don't have the necessary permissions to access this page.",
            )
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Place:
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Place, id=self.kwargs.get("place_id"))
        return self.object

    def get_props(self, request, *args, **kwargs):
        place = self.get_object()

        return {
            "education": EducationTinySerializer(place.education).data,
            "place": PlaceSerializer(place, context={"request": request}).data,
            "places": [{
                "id": place.id,
                "name": f"{place.education.short_name}: {place.name}",
            } for place in Place.objects.filter(contacts__user_id=request.user.id).select_related("education")],
        }

    def get_page_title(self, request, *args, **kwargs) -> str:
        return f"{self.get_object().name} - Stageplaats"
