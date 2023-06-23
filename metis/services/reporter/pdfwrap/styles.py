from pathlib import Path
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .types import FontFamily


DIR = Path(__file__).parent
panno = FontFamily("ugentpannotext-semilight-web", "ugentpannotext-medium-web")
panno_bold = FontFamily("ugentpannotext-medium-web")

for font_family in [panno, panno_bold]:
    for font in font_family:
        if font is None:
            continue
        pdfmetrics.registerFont(TTFont(font, DIR.parent.parent.parent / "site" / "static" / "fonts" / f"{font}.ttf"))

pdfmetrics.registerFontFamily(
    panno.normal,
    normal=panno.normal,
    bold=panno.bold,
    italic=panno.italic,
    boldItalic=panno.bold_italic,
)


UGENT_BLUE = "#1e64c8"
UGENT_YELLOW = "#ffd200"
ELIS_PURPLE = "#6f71b9"

TEXT_COLOR = "#15141A"
LIGHT_TEXT_COLOR = "#555555"
DARK_TEXT_COLOR = "#000000"

BASE_FONT_SIZE = 12
LINE_HEIGHT = 1.4

PDF_STYLES = {
    "default": ParagraphStyle(
        "default",
        fontName=panno.normal,
        fontSize=BASE_FONT_SIZE,
        leading=BASE_FONT_SIZE * LINE_HEIGHT,
        textColor=TEXT_COLOR,
    )
}

PDF_STYLES["p"] = ParagraphStyle(
    "p",
    PDF_STYLES["default"],
    spaceBefore=2 * mm,
    spaceAfter=2 * mm,
)

PDF_STYLES["p_justify"] = ParagraphStyle(
    "p_justify",
    PDF_STYLES["p"],
    alignment=TA_JUSTIFY,
    hyphenationLang="en_GB",
)

PDF_STYLES["p_right"] = ParagraphStyle(
    "p_right",
    PDF_STYLES["p"],
    alignment=TA_RIGHT,
)

PDF_STYLES["p_small"] = ParagraphStyle(
    "p_small",
    PDF_STYLES["p"],
    fontSize=9,
)

PDF_STYLES["footer"] = ParagraphStyle(
    "footer",
    PDF_STYLES["default"],
    fontSize=BASE_FONT_SIZE * 0.8,
    leading=BASE_FONT_SIZE * 0.8 * LINE_HEIGHT,
    textColor=LIGHT_TEXT_COLOR,
)

PDF_STYLES["ul_li"] = ParagraphStyle(
    "ul_li",
    PDF_STYLES["default"],
    bulletText="•",
    bulletIndent=3 * mm,
    leftIndent=6 * mm,
    spaceAfter=1 * mm,
)

PDF_STYLES["ol_li"] = ParagraphStyle(
    "ol_li",
    PDF_STYLES["ul_li"],
    bulletText="OL",
)

PDF_STYLES["h1"] = ParagraphStyle(
    "h1",
    PDF_STYLES["default"],
    fontName=panno_bold.normal,
    fontSize=23,
    leading=28,
    rightIndent=40 * mm,
    textColor=UGENT_BLUE,
    spaceAfter=7 * mm,
)

PDF_STYLES["h2"] = ParagraphStyle(
    "h2",
    PDF_STYLES["h1"],
    fontSize=16,
    leading=20,
    rightIndent=40 * mm,
)

PDF_STYLES["h3"] = ParagraphStyle(
    "h3",
    PDF_STYLES["default"],
    fontSize=14,
    leading=17,
)

PDF_STYLES["h4"] = ParagraphStyle(
    "h4",
    PDF_STYLES["h3"],
    fontSize=12,
    leading=14,
)

PDF_STYLES["h5"] = ParagraphStyle(
    "h5",
    PDF_STYLES["h3"],
    fontSize=12,
    leading=14,
)

PDF_STYLES["h6"] = ParagraphStyle(
    "h6",
    PDF_STYLES["default"],
    fontName=panno_bold.normal,
    spaceBefore=5 * mm,
)
