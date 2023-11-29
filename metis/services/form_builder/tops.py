from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, ValidationError

from .custom_forms import Translation


if TYPE_CHECKING:
    from metis.models.stages.projects import Project


class TopsForm(BaseModel):
    """A TOPS form."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    title: Translation | None = None
    task_cta: Translation | None = None
    description: Translation | None = None
    type: Literal["project_places", "regions"]
    triage_question: Translation | None = None
    num_tops: int
    require_motivation: bool = False


def validate_tops_form_definition(definition: dict) -> TopsForm:
    """Validate a tops form definition."""
    try:
        return TopsForm(**definition)
    except (TypeError, ValidationError) as exc:
        raise ValueError(exc) from exc


def validate_tops_form_response(form_definition: dict, data: dict, project: "Project") -> dict:
    """Validate form data against a form definition.

    Response data has this structure:
    {
        "tops": list[int],
        "motivation": {
            project_place_id (int): str,  # if TopsForm.require_motivation is True, for each project_place_id in "tops"
        },
    }
    """
    form = validate_tops_form_definition(form_definition)

    if not isinstance(data, dict) or "tops" not in data:
        raise ValueError("Response data should be a dict with a `tops` key")

    if form.triage_question and data["tops"] is None:
        return data

    if not isinstance(data.get("tops"), list):
        raise ValueError("Response data should contain a list of tops")

    if len(data["tops"]) != form.num_tops:
        raise ValueError("Invalid number of tops")

    if form.type == "project_places":
        project_place_ids = set(project.project_places.values_list("id", flat=True))
        for project_place_id in data["tops"]:
            if project_place_id not in project_place_ids:
                raise ValueError(f"Invalid ProjectPlace id `{project_place_id}`")
        if len(set(data["tops"])) != len(data["tops"]):
            raise ValueError("Duplicate ProjectPlace ids")

        if form.require_motivation:
            if not isinstance(data.get("motivation"), dict):
                raise ValueError("Missing required field `motivation`")
            keys = list(data["motivation"].keys())
            for project_place_id in data["tops"]:
                pp_id = str(project_place_id)
                if pp_id not in keys:
                    raise ValueError(f"Missing motivation for ProjectPlace id `{project_place_id}`")
                if not isinstance(data["motivation"][pp_id], str) or not data["motivation"][pp_id]:
                    raise ValueError(f"Invalid motivation for ProjectPlace id `{project_place_id}`")

    elif form.type == "regions":
        raise NotImplementedError("Regions form not implemented")

    return data
