import os

from django.conf import settings
from django.middleware.csrf import get_token as get_csrf_token
from django.utils.text import slugify
from django.views.generic import View
from inertia import render
from typing import Dict, Optional


def render_inertia(request, vue_entry_point: str, *, props: Optional[Dict] = None, page_title: Optional[str] = None):
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
            "django_locale": request.LANGUAGE_CODE,
            "django_user": request.user if request.user.is_authenticated else None,
            "git_commit_hash": os.environ.get("GIT_REV", "None"),
        }
        | (props or {}),
        template_data={
            "page_title": page_title or "Metis",
            "vue_entry_point": vue_entry_point,
        },
    )


class InertiaView(View):
    page_title: Optional[str] = None
    vue_entry_point = None

    def get_page_title(self, request, *args, **kwargs) -> Optional[str]:
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
            page_title=self.get_page_title(self, request, *args, **kwargs)
        )