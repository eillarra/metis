from io import BytesIO
from typing import NamedTuple

import pandas as pd
from django.http import HttpResponse


class ExcelSheet(NamedTuple):
    """A sheet of an Excel file."""

    name: str
    df: pd.DataFrame


class ExcelResponse(HttpResponse):
    """An HTTP response class that will send Excel content."""

    def __init__(self, *args, filename: str = "", **kwargs):
        kwargs.setdefault(
            "content_type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8"
        )
        super().__init__(*args, **kwargs)
        self["Content-Disposition"] = f'attachment; filename="{filename}"'


class Excel:
    """Generate an Excel file."""

    def get_filename(self) -> str:
        """Get the filename of the Excel file, without extension."""
        raise NotImplementedError

    def get_sheets(self) -> list[ExcelSheet]:
        """Get the sheets of the Excel file."""
        raise NotImplementedError

    def get_response(self) -> ExcelResponse:
        """Generate an Excel file with all the sheets."""
        buffer = BytesIO()

        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            for sheet in self.get_sheets():
                sheet.df.to_excel(writer, sheet_name=sheet.name, na_rep="-")

        buffer.seek(0)  # rewind the buffer

        return ExcelResponse(buffer.read(), filename=f"{self.get_filename()}.xlsx")
