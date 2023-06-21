import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph

from .styles import PDF_STYLES


class PdfWrap:
    def __init__(
        self, *, page_size: tuple = A4, margins: list[float] = [12 * mm, 12 * mm, 20 * mm, 12 * mm], styles=PDF_STYLES
    ) -> None:
        self.buffer = io.BytesIO()
        self.parts = []
        self.styles = styles
        self.footer_text: str | None = None
        self.footer_style = "footer"
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=page_size,
            topMargin=margins[0] - 6,  # compensate inner Frame padding (6 points)
            rightMargin=margins[1] - 6,
            bottomMargin=margins[2] - 6,
            leftMargin=margins[3] - 6,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.buffer.close()

    def _draw_footer(self, canvas, doc) -> None:
        if not self.footer_text:
            return

        canvas.saveState()
        footer = Paragraph(self.footer_text, self.styles[self.footer_style])
        _, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin + (2 * mm), h + 5 * mm)
        canvas.restoreState()

    def _first_page(self, canvas, doc) -> None:
        self._draw_footer(canvas, doc)

    def _later_pages(self, canvas, doc) -> None:
        self._draw_footer(canvas, doc)

    def add_footer(self, text: str, style: str = "footer") -> None:
        self.footer_style = style
        self.footer_text = text

    def add_paragraph(self, text: str, style: str = "p") -> None:
        self.parts.append(Paragraph(text, self.styles[style]))

    def add_page_break(self) -> None:
        self.parts.append(PageBreak())

    def get_data(self) -> bytes:
        self.doc.build(self.parts, onFirstPage=self._first_page, onLaterPages=self._later_pages)
        return self.buffer.getvalue()
