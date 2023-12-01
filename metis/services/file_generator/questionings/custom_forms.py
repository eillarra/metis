from typing import TYPE_CHECKING

import pandas as pd

from metis.services.form_builder.custom_forms import CustomForm

from ..excel import ExcelSheet


if TYPE_CHECKING:
    from metis.models.stages import Questioning


def get_custom_form_sheets(questioning: "Questioning") -> list["ExcelSheet"]:
    """Generate an Excel file with responses from project place information questionings."""
    form = CustomForm(**questioning.form_definition)
    questioning_responses = questioning.responses.all()
    columns = ["obj", "created_by", "created_at"]
    rows = []

    for field in form.get_fields():
        columns.append(field.code)

    for response in questioning_responses:
        res = {
            "obj": str(response.content_object),
            "created_by": response.created_by.name,
            "created_at": str(response.created_at),
        }

        for field in form.get_fields():
            res[field.code] = response.data.get(field.code, "")

        rows.append(res)

    df = pd.DataFrame(rows, columns=columns)
    df = df.fillna("")

    return [ExcelSheet(name=questioning.title, df=df)]
