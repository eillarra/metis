from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import View
from requests.exceptions import HTTPError

from metis.models.rel.files import File
from metis.services.s3 import get_s3_response


class MediaFileView(View):
    """
    Serves private S3 files, checking user permissions beforehand if needed.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_file_access(self.get_object()):  # type: ignore
            raise PermissionDenied("You don't have the necessary permissions to access this file.")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self) -> File:
        if not hasattr(self, "object"):
            self.object = get_object_or_404(File, file=self.request.path.replace("/media/", "", 1))
        return self.object

    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        file = self.get_object()

        try:
            res = get_s3_response(file.s3_object_key)
        except HTTPError:
            raise Http404("File not found.")

        return HttpResponse(
            res.raw,
            headers={
                "Content-Disposition": f'inline; filename="{file.file.name}"',
                "Content-Length": res.headers["Content-Length"],
                "Content-Type": res.headers["Content-Type"],
            },
        )
