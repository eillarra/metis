import pandas as pd
from django.utils.text import slugify

from metis.models import Project

from ..excel import Excel, ExcelSheet


class ProjectContactsExcel(Excel):
    """Generate an Excel file with an overview of the project contacts."""

    def __init__(self, project: Project):
        self.project = project

    def get_filename(self) -> str:
        """Get the filename of the Excel file, without extension."""
        filename = "_".join(
            [
                "metis",
                self.project.education.code,
                self.project.name,
                "contacts",
            ]
        )
        return slugify(filename)

    def get_sheets(self) -> list[ExcelSheet]:
        """Generate an Excel file with all periods of a project."""
        sheets = []

        columns = [
            "place_name",
            "name",
            "email",
            "phone_numbers",
            "is_admin",
            "is_mentor",
            "last_login",
        ]

        rows = []

        for place in self.project.places.all():
            for contact in place.contacts.all():
                rows.append(
                    {
                        "place_name": place.name,
                        "name": contact.user.name,
                        "email": contact.user.email,
                        "phone_numbers": [p.number for p in contact.user.phone_numbers.all()],
                        "is_admin": contact.is_admin,
                        "is_mentor": contact.is_mentor,
                        "last_login": str(contact.user.last_login),
                    }
                )

        df = pd.DataFrame(rows, columns=columns)
        df = df.fillna("")
        df = df.set_index(["place_name"])

        sheets.append(ExcelSheet(name="CONTACTS", df=df))

        return sheets
