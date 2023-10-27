from pydantic import BaseModel, field_validator

from .custom_forms import Translation


class EvaluationGrade(BaseModel):
    value: int | None
    label: Translation


class EvaluationItem(BaseModel):
    value: str
    label: Translation


class EvaluationSection(BaseModel):
    code: str
    title: Translation | None = None
    description: Translation | None = None
    items: list[EvaluationItem] = []
    cross_items: list[EvaluationItem] = []
    add_remarks: bool = True


class EvaluationForm(BaseModel):
    title: Translation | None = None
    description: Translation | None = None
    intermediate_evaluations: int = 0
    global_section_evaluation: bool = True
    global_evaluation: bool = True
    grades: list[EvaluationGrade] = []
    sections: list[EvaluationSection] = []

    @field_validator("grades")
    def validate_grades(cls, v):
        values = set()
        for grade in v:
            if grade.value in values:
                raise ValueError(f"Duplicate grade value `{grade.value}`")
            values.add(grade.value)
        return v
