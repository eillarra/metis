from pydantic import BaseModel, ConfigDict, ValidationError, field_validator
from pydantic.types import conlist

from .custom_forms import Translation


class EvaluationScore(BaseModel):
    """A score for an evaluation form."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    value: str | None
    label: Translation
    points: int | float | None
    only_for_global_score: bool = False


class EvaluationItem(BaseModel):
    """An item in an evaluation form."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    value: str
    label: Translation


class EvaluationSection(BaseModel):
    """A section in an evaluation form."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    code: str
    title: Translation | None = None
    description: Translation | None = None
    items: conlist(EvaluationItem, min_length=1)  # type: ignore
    cross_items: list[EvaluationItem] = []
    with_remarks: bool = False


class EvaluationForm(BaseModel):
    """An evaluation form."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    title: Translation | None = None
    description: Translation | None = None
    intermediate_evaluations: int = 0
    scores: conlist(EvaluationScore, min_length=2)  # type: ignore
    sections: conlist(EvaluationSection, min_length=1)  # type: ignore
    with_global_remarks: bool = True

    @field_validator("scores")
    def validate_scores(cls, v):
        """Validate scores checking for duplicate values."""
        values, points = set(), set()
        for score in v:
            if score.value in values:
                raise ValueError(f"Duplicate score value `{score.value}`")
            if score.points in points:
                raise ValueError(f"Duplicate score points `{score.points}` for score `{score.value}")
            values.add(score.value)
            points.add(score.points)
        return v

    def get_valid_scores(self, *, section_only: bool = False) -> set[str]:
        """Return a set of valid score values.

        Parameters:
            section_only: if True, only return the score values for sections
        """
        if section_only:
            return {score.value for score in self.scores if not score.only_for_global_score}
        return {score.value for score in self.scores}


def validate_evaluation_form_definition(definition: dict) -> EvaluationForm:
    """Validate an evaluation form definition."""
    try:
        return EvaluationForm(**definition)
    except (TypeError, ValidationError) as exc:
        raise ValueError(exc) from exc


def validate_evaluation_form_response(form_definition: dict, data: dict) -> dict:
    """Validate evaluation data against an evaluation form definition.

    Response data has this structure:
    {
        "global_remarks": str,  # if EvaluationForm.with_global_remarks is True
        "global_score": str,
        "sections": {
            section.code (str): {
                "remarks": str,  # if EvaluationSection.with_remarks is True
                "score": str,
                "scores": {
                    item.value (str): (str, None) or (str, "cross"),  # depending on EvaluationSection.cross_items
                },
            },
        },
    }
    """
    form = validate_evaluation_form_definition(form_definition)
    valid_section_scores = form.get_valid_scores(section_only=True)
    valid_scores = form.get_valid_scores()

    if not isinstance(data, dict) or "sections" not in data:
        raise ValueError("Response data should be a dict with a `sections` key")

    if not isinstance(data["sections"], dict):
        raise ValueError("Response data should contain a dict of sections")

    if "global_score" not in data or data["global_score"] not in valid_scores:
        raise ValueError("Missing a valid `global_score`")

    if form.with_global_remarks and "global_remarks" not in data or not isinstance(data["global_remarks"], str):
        raise ValueError("Missing valid `global_remarks`")

    for section in form.sections:
        if section.code not in data["sections"] or not isinstance(data["sections"][section.code], dict):
            raise ValueError(f"Missing response for section `{section.code}`")

        if (
            "score" not in data["sections"][section.code]
            or data["sections"][section.code]["score"] not in valid_section_scores
        ):
            raise ValueError(f"Missing valid `score` for section `{section.code}`")

        if section.with_remarks and (
            "remarks" not in data["sections"][section.code]
            or not isinstance(data["sections"][section.code]["remarks"], str)
        ):
            raise ValueError(f"Missing valid `remarks` for section `{section.code}`")

    return data
