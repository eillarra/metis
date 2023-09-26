import os

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


class PdfResponse(HttpResponse):
    def __init__(self, content: bytes = b"", as_attachment: bool = False, filename: str = "", *args, **kwargs):
        self.as_attachment = as_attachment
        self.filename = filename
        kwargs.setdefault("content_type", "application/pdf")
        super().__init__(content, *args, **kwargs)


def django_link_callback(uri, rel) -> str:
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """

    static_url = settings.STATIC_URL
    static_root = settings.STATIC_ROOT
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT

    if uri.startswith(media_url):
        path = media_root / uri.replace(media_url, "")
    elif uri.startswith(static_url):
        path = static_root / uri.replace(static_url, "")
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception("Please make sure that file exists: {}".format(path))

    return str(path)


def render_pdf_template(request: HttpRequest, template_path: str, context: dict) -> HttpResponse:
    response = PdfResponse()
    template = get_template(template_path)
    html = template.render(context)
    pisa.pisaDocument(html, dest=response, link_callback=django_link_callback)
    return response
