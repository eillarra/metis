from typing import TYPE_CHECKING

import pandas as pd

from .base import ExcelSheet


if TYPE_CHECKING:
    from metis.models.stages import Questioning


def get_student_tops_sheets(questioning: "Questioning") -> list["ExcelSheet"]:
    """Generate an Excel file with responses from student tops questionings."""
    period = questioning.period
    project_places = period.project_places.order_by("place__name")
    students = period.students.order_by("user__last_name", "user__first_name")
    updated_at = {}
    tops = {}

    for student in students:
        form_response = student.form_responses.filter(
            questioning__type="student_tops", questioning__period_id=period.id
        ).first()
        student_tops = form_response.data["tops"] if form_response else []
        updated_at[student.id] = str(form_response.updated_at) if form_response else None
        tops[student.id] = {}

        for index, project_place_id in enumerate(student_tops):
            tops[student.id][project_place_id] = index + 1

    df = pd.DataFrame(
        [[tops[student.id].get(project_place.id, "-") for project_place in project_places] for student in students],
        columns=[project_place.place.name for project_place in project_places],
        index=pd.MultiIndex.from_tuples([(updated_at[student.id], student.reverse_name) for student in students]),
    )

    return [ExcelSheet(name="Tops", df=df)]
