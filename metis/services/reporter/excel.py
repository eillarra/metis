import pandas as pd

from django.http import HttpResponse
from io import BytesIO

from metis.models import Period


class ExcelResponse(HttpResponse):
    def __init__(self, *args, filename: str = "", **kwargs):
        kwargs.setdefault(
            "content_type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8"
        )
        super().__init__(*args, **kwargs)
        self["Content-Disposition"] = f'attachment; filename="{filename}"'


class StudentTopsExcel:
    def __init__(self, period_id: int):
        self.period = Period.objects.get(id=period_id)

    def get_response(self):
        """
        Project places are columns and students are rows
        the rows then show the top choices of the students (place_ids)
        """

        project_places = self.period.project_places.order_by("place__name")
        students = self.period.students.order_by("user__last_name", "user__first_name")
        updated_at = {}
        tops = {}

        for student in students:
            form_response = student.form_responses.filter(form__code="student_tops").first()
            student_tops = form_response.data["tops"] if form_response else []
            updated_at[student.id] = str(form_response.updated_at) if form_response else None
            tops[student.id] = {}

            for index, project_place_id in enumerate(student_tops):
                tops[student.id][project_place_id] = index + 1

        df = pd.DataFrame(
            [[tops[student.id].get(project_place.id, "-") for project_place in project_places] for student in students],
            columns=[project_place.place.name for project_place in project_places],
            index=pd.MultiIndex.from_tuples(
                [
                    (updated_at[student.id], f"{student.user.last_name}, {student.user.first_name}")
                    for student in students
                ]
            ),
        )

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer)
        buffer.seek(0)

        return ExcelResponse(buffer.read(), filename="student_tops.xlsx")
