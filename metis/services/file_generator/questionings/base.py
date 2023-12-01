from django.utils.text import slugify

from metis.models import Questioning

from ..excel import Excel, ExcelSheet
from .custom_forms import get_custom_form_sheets
from .student_tops import get_student_tops_sheets


class QuestioningExcel(Excel):
    """Generate an Excel file with all the responses of a questioning."""

    def __init__(self, questioning: Questioning):
        self.questioning = questioning

    def get_filename(self) -> str:
        """Get the filename of the Excel file, without extension."""
        filename = "_".join(
            [
                "metis",
                self.questioning.project.education.code,
                self.questioning.project.name,
                self.questioning.period.full_name if self.questioning.period else "",
                "q",
                str(self.questioning.pk),
                self.questioning.type,
            ]
        )
        return slugify(filename)

    def get_sheets(self) -> list[ExcelSheet]:
        """Generate an Excel file with all the responses of a questioning, based on type."""
        try:
            sheets = {
                Questioning.PROJECT_PLACE_INFORMATION: get_custom_form_sheets,
                Questioning.STUDENT_INFORMATION: get_custom_form_sheets,
                Questioning.STUDENT_TOPS: get_student_tops_sheets,
            }[self.questioning.type](self.questioning)
        except KeyError as exc:
            raise NotImplementedError(f"Questioning type `{self.questioning.type}` has no Excel generator.") from exc

        return sheets
