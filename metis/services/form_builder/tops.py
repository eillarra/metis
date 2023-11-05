from typing import Literal

from pydantic import BaseModel

from .custom_forms import Translation


class TopsForm(BaseModel):
    title: Translation | None = None
    description: Translation | None = None
    type: Literal["project_places", "regions"]
    num_tops: int
