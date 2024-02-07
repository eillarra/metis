from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import View
from requests.exceptions import HTTPError

from metis.models.rel.files import File
from metis.models.stages import Internship, Project
from metis.services.s3 import get_s3_response


class MediaFileBaseView(View):
    """Base view for serving private S3 files."""

    def get_object(self) -> File:
        """Get the file object."""
        if not hasattr(self, "object"):
            print(self.kwargs.get("file"))
            self.object = get_object_or_404(File, file=self.kwargs.get("file"))
        return self.object

    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        """Serve the file."""
        file = self.get_object()

        try:
            res = get_s3_response(file.s3_object_key)
        except HTTPError as exc:
            raise Http404("File not found.") from exc

        return HttpResponse(
            res.raw,
            headers={
                "Content-Disposition": f'inline; filename="{file.file.name}"',
                "Content-Length": res.headers["Content-Length"],
                "Content-Type": res.headers["Content-Type"],
            },
        )


class MediaFileView(MediaFileBaseView):
    """Private view for serving private S3 files.

    Permissions are checked if needed.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if not request.user.has_file_access(self.get_object()):  # type: ignore
            raise PermissionDenied("You don't have the necessary permissions to access this file.")
        return super().dispatch(request, *args, **kwargs)


class InternshipMediaFileSecretView(MediaFileBaseView):
    """Private view for serving private S3 files, accessed using a secret link for internships.

    Only relation between Internship and File content_object is checked.
    """

    def get_internship(self):
        """Get the internship."""
        if not hasattr(self, "internship"):
            self.internship = get_object_or_404(Internship, uuid=self.kwargs.get("uuid"))
        return self.internship

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        content_object = self.get_object().content_object

        if isinstance(content_object, Internship) and content_object != self.get_internship():
            raise PermissionDenied("You don't have the necessary permissions to access this file.")

        if isinstance(content_object, Project) and content_object != self.get_internship().project:
            raise PermissionDenied("You don't have the necessary permissions to access this file.")

        return super().dispatch(request, *args, **kwargs)
