from typing import Literal

from pydantic import BaseModel, ConfigDict

from .custom_forms import Translation


class TopsForm(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True)

    title: Translation | None = None
    task_cta: Translation | None = None
    description: Translation | None = None
    type: Literal["project_places", "regions"]
    triage_question: Translation | None = None
    num_tops: int
    require_motivation: bool = False
