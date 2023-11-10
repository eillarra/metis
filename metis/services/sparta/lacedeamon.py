from django.db.models import QuerySet

from .models import SpartaInternship, SpartaStudent


class Lacedeamon:
    """This class is responsible for the data retrieval from the legacy SPARTA database.

    Data can be retrieved using some simple Django models and the Django ORM,
    and then shared with DICT using a standard API.

    Lacedeamon was the son of Zeus. He was the king of Sparta.
    """

    projects: dict[tuple[str, int], int] = {
        ("geneeskunde", 2020): 10,
        ("geneeskunde", 2021): 10,
        ("geneeskunde", 2022): 12,
        ("geneeskunde", 2023): 14,
        ("geneeskunde", 2024): 16,
        ("revaki", 2022): 11,
        ("revaki", 2023): 13,
        ("revaki", 2024): 15,
    }

    def __init__(self, education_code: str, year: int = 2024) -> None:
        try:
            self.project_id = self.projects[(education_code, year)]
            self.education_code = education_code
            self.year = year
        except KeyError as err:
            raise ValueError(f"No project found for education code {education_code} and year {year}") from err

    def get_internships(self) -> QuerySet["SpartaInternship"]:
        """Return a list of internships."""
        return SpartaInternship.objects.filter(project=self.project_id).select_related("discipline", "student")

    def get_students(self) -> QuerySet["SpartaStudent"]:
        """Return a list of students."""
        return SpartaStudent.objects.filter(project=self.project_id)
