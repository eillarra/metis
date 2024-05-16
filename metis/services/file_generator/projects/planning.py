import pandas as pd
from django.utils.text import slugify

from metis.models import Period, Project

from ..excel import Excel, ExcelSheet


class ProjectPlanningExcel(Excel):
    """Generate an Excel file with an overview of the project planning."""

    def __init__(self, project: Project):
        self.project = project

    def get_filename(self) -> str:
        """Get the filename of the Excel file, without extension."""
        filename = "_".join(
            [
                "metis",
                self.project.education.code,
                self.project.name,
                "planning",
            ]
        )
        return slugify(filename)

    def get_sheets(self) -> list[ExcelSheet]:
        """Generate an Excel file with all periods of a project."""
        sheets = []

        for period in self.project.periods.all():
            sheets += get_period_sheet(period)

        return sheets


def get_period_sheet(period: "Period") -> list["ExcelSheet"]:
    """Generate an Excel sheet with all the internships of a period."""
    columns = [
        "student_number",
        "student_name",
        "student_email",
        "period",
        "track",
        "status",
        "discipline",
        "start_date",
        "end_date",
        "place_name",
        "total_hours",
        "final_score",
        "place_admin",
        "admin_email",
        "mentors",
        "mentor_emails",
    ]
    rows = []

    internships = (
        period.internships.prefetch_related(
            "discipline", "track", "place__contacts", "mentors", "student__user", "timesheets"
        )
        .order_by("student__user__last_name", "student__user__first_name")
        .all()
    )

    for internship in internships:
        admin = internship.place.contacts.filter(is_admin=True).first() if internship.place else None
        mentors = internship.mentors.all()
        total_hours = internship.total_hours
        formatted_hours = f"{total_hours[0]:02d}:{total_hours[1]:02d}"

        internship_data = {
            "student_number": internship.student.number,
            "student_name": internship.student.reverse_name,
            "student_email": internship.student.user.email,
            "period": period.full_name,
            "track": internship.track.name,
            "status": internship.status,
            "discipline": internship.discipline.name,
            "start_date": internship.start_date,
            "end_date": internship.end_date,
            "place_name": internship.place.name if internship.place else "-",
            "total_hours": formatted_hours,
            "final_score": internship.final_score or "-",
            "place_admin": admin.user.name if admin else "",
            "admin_email": admin.user.email if admin else "",
            "mentors": ", ".join([mentor.user.name for mentor in mentors]),
            "mentor_emails": ", ".join([mentor.user.email for mentor in mentors]),
        }

        rows.append(internship_data)

    df = pd.DataFrame(rows, columns=columns)
    df = df.fillna("")
    df = df.set_index(["student_number"])

    return [ExcelSheet(name=slugify(period.full_name).upper(), df=df)]
