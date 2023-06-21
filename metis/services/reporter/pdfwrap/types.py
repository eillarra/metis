from typing import NamedTuple


class FontFamily(NamedTuple):
    normal: str
    bold: str | None = None
    italic: str | None = None
    bold_italic: str | None = None
