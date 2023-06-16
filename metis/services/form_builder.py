from enum import Enum
from pydantic import BaseModel, Extra, ValidationError, validator
from typing import Literal, Union


class DayOfWeek(Enum):
    maandag = "maandag"
    dinsdag = "dinsdag"
    woensdag = "woensdag"
    donderdag = "donderdag"
    vrijdag = "vrijdag"
    zaterdag = "zaterdag"
    zondag = "zondag"


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


class TimetableField(FormField):
    type: Literal["timetable"]
    days: list[DayOfWeek]


class Fieldset(BaseModel):
    fields: list[Union[InputField, ChoiceField, TimetableField]]
    legend: Translation | None = None
    description: Translation | None = None

    class Config:
        extra = Extra.forbid
        validate_all = True


class Form(BaseModel):
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


def validate_form_definition(definition: dict) -> Form:
    """
    Validate a form definition.
    """

    try:
        return Form(**definition)
    except (TypeError, ValidationError) as e:
        raise ValueError(e)


def validate_form_data(form_definition: dict, data: dict) -> dict:
    """
    Validate form data against a form definition.
    """

    form = validate_form_definition(form_definition)
    fields = []
    field_codes = set()
    required_field_codes = set()

    if not isinstance(data, dict):
        raise ValueError("Data should be a dict")

    for fieldset in form.fieldsets:
        for field in fieldset.fields:
            fields.append(field)
            field_codes.add(field.code)
            if type(field) == ChoiceField and field.other_option:
                field_codes.add(f"{field.code}__{field.other_option}")
            if field.required:
                required_field_codes.add(field.code)

    for field in data:
        if field not in field_codes:
            raise ValueError(f"Unknown field `{field}`")

    missing_fields = required_field_codes - set(data.keys())
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")

    for field in fields:
        if field.type in {"select", "option_group"} and field.code in data:
            options = {option.value for option in field.options}

            if field.multiple:
                if not isinstance(data[field.code], list):
                    raise ValueError(f"Field `{field.code}` should be a list")
                for value in data[field.code]:
                    if value not in options:
                        raise ValueError(f"Invalid value `{value}` for field `{field.code}`")
            else:
                if data[field.code] not in options:
                    raise ValueError(f"Invalid value `{data[field.code]}` for field `{field.code}`")

            if field.other_option and field.other_option in data[field.code]:
                other_code = f"{field.code}__{field.other_option}"
                if other_code not in data or not isinstance(data[other_code], str):
                    raise ValueError(f"Field `{field.code}__{field.other_option}` should be defined, as a string")

        elif field.type in {"timetable"} and field.code in data:
            if not isinstance(data[field.code], str):
                raise ValueError(f"Field `{field.code}` should be a list")

        elif field.code in data:
            if not isinstance(data[field.code], str):
                raise ValueError(f"Field `{field.code}` should be a string")

    return data
