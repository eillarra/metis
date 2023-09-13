from pydantic import BaseModel, Extra, validator
from typing import Literal, Union


class Translation(BaseModel):
    nl: str
    en: str


class Rule(BaseModel):
    field: str
    type: Literal["equals", "not_equals", "contains", "not_contains", "is_empty", "is_not_empty"]
    value: str | int | bool | None = None

    class Config:
        extra = Extra.forbid
        validate_default = True


class FieldOption(BaseModel):
    value: str | int
    label: Translation

    class Config:
        extra = Extra.forbid
        validate_default = True


class FormField(BaseModel):
    type: str
    code: str
    label: Translation
    required: bool = False
    collapsed: bool = False

    class Config:
        validate_default = True


class InputField(FormField):
    type: Literal["text", "textarea", "number", "date", "email", "tel", "url"]
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
    rule: Rule | None = None

    class Config:
        extra = Extra.forbid
        validate_default = True


class CustomForm(BaseModel):
    fieldsets: list[Fieldset]
    title: Translation | None = None
    description: Translation | None = None

    class Config:
        extra = Extra.forbid
        validate_default = True

    @validator("fieldsets")
    def validate_fieldsets(cls, v):
        codes = set()
        for fieldset in v:
            for field in fieldset.fields:
                if field.code in codes:
                    raise ValueError(f"Duplicate field code `{field.code}`")
                codes.add(field.code)
        return v
