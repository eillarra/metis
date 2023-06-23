import os

from django.conf import settings
from django.middleware.csrf import get_token as get_csrf_token
from django.utils.text import slugify
from django.views.generic import View
from inertia import render


def render_inertia(request, vue_entry_point: str, *, props: dict | None = None, page_title: str | None = None):
    """
    Render a Vue component with Inertia.
    It adds some basic props that can be helpful.
    """

    return render(
        request,
        slugify(vue_entry_point),
        props={
            "django_csrf_token": get_csrf_token(request),
            "django_debug": settings.DEBUG,
            "django_env": os.environ.get("DJANGO_ENV", "development"),
            "django_locale": request.LANGUAGE_CODE,
            "django_user": request.user if request.user.is_authenticated else None,
            "git_commit_hash": os.environ.get("GIT_REV", None),
            "mapbox_token": os.environ.get("MAPBOX_TOKEN", ""),
        }
        | (props or {}),
        template_data={
            "page_title": page_title or "Metis",
            "vue_entry_point": vue_entry_point,
        },
    )


class InertiaView(View):
    page_title: str | None = None
    vue_entry_point: str | None = None

    def get_page_title(self, request, *args, **kwargs) -> str | None:
        return self.page_title

    def get_props(self, request, *args, **kwargs):
        return {}

    def get(self, request, *args, **kwargs):
        if self.vue_entry_point is None:
            raise NotImplementedError("`vue_entry_point` must be set")

        return render_inertia(
            request,
            self.vue_entry_point,
            props=self.get_props(request, *args, **kwargs),
            page_title=self.get_page_title(self, request, *args, **kwargs),
        )
