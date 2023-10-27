from pydantic import BaseModel, ConfigDict, field_validator
from typing import Generator, Literal, Union


class Translation(BaseModel):
    nl: str
    en: str


class Rule(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True)

    field: str
    type: Literal["equals", "not_equals", "contains", "not_contains", "is_empty", "is_not_empty"]
    value: str | int | bool | None = None


class FieldOption(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True)

    value: str | int
    label: Translation


class FormField(BaseModel):
    model_config = ConfigDict(validate_default=True)

    type: str
    code: str
    label: Translation
    required: bool = False
    collapsed: bool = False


class InputField(FormField):
    type: Literal["text", "textarea", "number", "date", "email", "tel", "url"]
    mask: str | None = None
    placeholder: Translation | None = None


class ChoiceField(FormField):
    type: Literal["select", "option_group"]
    options: list[FieldOption]
    multiple: bool = False
    other_option: str | None = None

    @field_validator("options")
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
    model_config = ConfigDict(extra="forbid", validate_default=True)

    fields: list[Union[InputField, ChoiceField, GridField]]
    legend: Translation | None = None
    description: Translation | None = None
    rule: Rule | None = None


class CustomForm(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True)

    fieldsets: list[Fieldset]
    title: Translation | None = None
    description: Translation | None = None

    @field_validator("fieldsets")
    def validate_fieldsets(cls, v):
        codes = set()
        for fieldset in v:
            for field in fieldset.fields:
                if field.code in codes:
                    raise ValueError(f"Duplicate field code `{field.code}`")
                codes.add(field.code)
        return v

    def get_fields(self) -> Generator[FormField, None, None]:
        for fieldset in self.fieldsets:
            for field in fieldset.fields:
                yield field
