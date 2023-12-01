from io import BytesIO
from typing import NamedTuple

import pandas as pd
from django.http import HttpResponse

from metis.models import Period


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


class PeriodIntershipsExcel:
    """Generate an Excel file with all the internships of a period."""

    def __init__(self, period: Period) -> None:
        self.period = period

    def get_response(self) -> HttpResponse:
        """Generate an Excel file with all the internships of a period."""
        columns = [
            "status",
            "student_number",
            "student_name",
            "student_email",
            "place_name",
            "place_admin",
            "admin_email",
            "mentors",
            "mentor_emails",
        ]
        rows = []

        for internship in self.period.internships.all():
            admin = internship.place.contacts.filter(is_admin=True).first()
            mentors = internship.mentors.all()
            internship_data = {
                "status": internship.status,
                "student_number": internship.student.number,
                "student_name": internship.student.user.name,
                "student_email": internship.student.user.email,
                "place_name": internship.place.name,
                "place_admin": admin.user.name if admin else "",
                "admin_email": admin.user.email if admin else "",
                "mentors": ", ".join([mentor.user.name for mentor in mentors]),
                "mentor_emails": ", ".join([mentor.user.email for mentor in mentors]),
            }

            rows.append(internship_data)

        df = pd.DataFrame(rows, columns=columns)
        df = df.fillna("")
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer)
        buffer.seek(0)

        return ExcelResponse(buffer.read(), filename=f"p{self.period.pk}_internships.xlsx")
