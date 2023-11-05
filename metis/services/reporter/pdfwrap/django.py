try:
    from django.http import HttpResponse
except ImportError as exc:
    raise ImportError("Django is required for the PdfResponse class") from exc


class PdfResponse(HttpResponse):
    def __init__(self, content: bytes, as_attachment: bool = False, filename: str = "", *args, **kwargs):
        self.as_attachment = as_attachment
        self.filename = filename
        kwargs.setdefault("content_type", "application/pdf")
        super().__init__(content, *args, **kwargs)
