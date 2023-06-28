from pydantic import BaseModel, Extra, validator
from typing import Literal, Union


class Translation(BaseModel):
    nl: str
    en: str


class FieldOption(BaseModel):
    value: str | int
    label: Translation

    class Config:
        extra = Extra.forbid
        validate_all = True


class FormField(BaseModel):
    type: str
    code: str
    label: Translation
    required: bool = False
    collapsed: bool = False

    class Config:
        validate_all = True


class InputField(FormField):
    type: Literal["text", "number", "date", "email", "tel", "url"]
    mask: str | None = None
    placeholder: Translation | None = None


class ChoiceField(FormField):
    type: Literal["select", "option_group"]
    options: list[FieldOption]
    multiple: bool = False
    other_option: str | None = None

    @validator("options")
    def validate_options(cls, v):
        values = set()
        for option in v:
            if option.value in values:
                raise ValueError(f"Duplicate option value `{option.value}`")
            values.add(option.value)
        return v


class GridField(FormField):
    type: Literal["option_grid"]
    options: list[FieldOption]
    columns: list[FieldOption]


class Fieldset(BaseModel):
    fields: list[Union[InputField, ChoiceField, GridField]]
    legend: Translation | None = None
    description: Translation | None = None

    class Config:
        extra = Extra.forbid
        validate_all = True


class CustomForm(BaseModel):
    fieldsets: list[Fieldset]
    title: Translation | None = None
    description: Translation | None = None

    class Config:
        extra = Extra.forbid
        validate_all = True

    @validator("fieldsets")
    def validate_fieldsets(cls, v):
        codes = set()
        for fieldset in v:
            for field in fieldset.fields:
                if field.code in codes:
                    raise ValueError(f"Duplicate field code `{field.code}`")
                codes.add(field.code)
        return v
