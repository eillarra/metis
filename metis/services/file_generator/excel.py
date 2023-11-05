from io import BytesIO

import pandas as pd
from django.http import HttpResponse

from metis.models import Questioning
from metis.services.form_builder.custom_forms import CustomForm


class ExcelResponse(HttpResponse):
    def __init__(self, *args, filename: str = "", **kwargs):
        kwargs.setdefault(
            "content_type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8"
        )
        super().__init__(*args, **kwargs)
        self["Content-Disposition"] = f'attachment; filename="{filename}"'


class QuestioningExcel:
    def __init__(self, questioning: Questioning):
        self.questioning = questioning

    def get_response(self):
        form = CustomForm(**self.questioning.form_definition)
        responses = self.questioning.responses.all()
        columns = ["place", "created_by", "created_at"]
        rows = []

        for field in form.get_fields():
            columns.append(field.code)

        for response in responses:
            res = {
                "place": response.content_object.place.name,  # TODO: this is not always a place
                "created_by": response.created_by.name,
                "created_at": str(response.created_at),
            }

            for field in form.get_fields():
                res[field.code] = response.data.get(field.code, "")

            rows.append(res)

        df = pd.DataFrame(rows, columns=columns)
        df = df.fillna("")

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer)
        buffer.seek(0)

        return ExcelResponse(buffer.read(), filename=f"{self.questioning.type}_q{self.questioning.id}.xlsx")
