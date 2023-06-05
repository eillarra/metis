from pydantic import BaseModel, Extra, ValidationError, validator


class Translation(BaseModel):
    nl: str
    en: str


class TextEntryType(BaseModel):
    code: str
    title: Translation

    class Config:
        extra = Extra.forbid
        anystr_strip_whitespace = True


class ProjectTextEntryType(TextEntryType):
    signature_required: bool = True


class PlaceTextEntryType(TextEntryType):
    editable_by_place: bool = True


class EducationConfig(BaseModel):
    allow_different_blocks_per_user_in_project: bool = True
    project_text_types: list[ProjectTextEntryType]
    place_text_types: list[PlaceTextEntryType] = []
    place_set_disciplines_per_block: bool = False

    class Config:
        extra = Extra.forbid
        validate_all = True

    @validator("project_text_types")
    def validate_project_text_types(cls, v):
        required = {"project.internship_agreement", "project.privacy_agreement"}
        codes = {c.code for c in v}
        for code in required:
            if code not in codes:
                raise ValueError(f"`project_text_types` must contain and entry with code `{code}`")
        return v


def validate_education_configuration(config):
    try:
        EducationConfig(**config)
    except (TypeError, ValidationError) as e:
        raise ValueError(e)
