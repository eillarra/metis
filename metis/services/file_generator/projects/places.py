import pandas as pd
from django.utils.text import slugify

from metis.models import Project

from ..excel import Excel, ExcelSheet


class ProjectPlacesExcel(Excel):
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
                "places",
            ]
        )
        return slugify(filename)

    def get_sheets(self) -> list[ExcelSheet]:
        """Generate an Excel file with all periods of a project."""
        sheets = []

        columns = [
            "place_name",
            "place_type",
            "is_flagged",
        ]

        rows = []

        for place in self.project.places.all():
            rows.append(
                {
                    "place_name": place.name,
                    "place_type": place.type.name if place.type else "-",
                    "is_flagged": place.is_flagged,
                }
            )

        df = pd.DataFrame(rows, columns=columns)
        df = df.fillna("")

        sheets.append(ExcelSheet(name="PLACES", df=df))

        return sheets
