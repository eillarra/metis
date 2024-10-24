from collections.abc import Generator
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from metis.utils.html import sanitize


class Translation(BaseModel):
    """A translation for a field label or description."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    nl: str
    en: str


class Rule(BaseModel):
    """A rule to show or hide a fieldset."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    field: str
    type: Literal["equals", "not_equals", "contains", "not_contains", "is_empty", "is_not_empty"]
    value: str | int | bool | None = None


class FieldOption(BaseModel):
    """An option for a choice field."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    value: str | int
    label: Translation


class FormField(BaseModel):
    """A field in a form."""

    model_config = ConfigDict(validate_default=True)

    type: str
    code: str
    label: Translation
    required: bool = False
    collapsed: bool = False


class InputField(FormField):
    """An input field in a form."""

    type: Literal["text", "textarea", "number", "date", "time", "email", "tel", "url"]
    mask: str | None = None
    placeholder: Translation | None = None


class ChoiceField(FormField):
    """A choice field in a form."""

    type: Literal["select", "option_group"]
    options: list[FieldOption]
    multiple: bool = False
    other_option: str | None = None
    other_label: Translation | None = None

    @field_validator("options")
    def validate_options(cls, v):
        """Validate options checking for duplicate option values."""
        values = set()
        for option in v:
            if option.value in values:
                raise ValueError(f"Duplicate option value `{option.value}`")
            values.add(option.value)
        return v


class GridField(FormField):
    """A grid field in a form."""

    type: Literal["option_grid"]
    options: list[FieldOption]
    rows: list[FieldOption]
    multiple: bool = True

    @property
    def all_options(self) -> list[str]:
        """Get all possible options for this grid field for multiple choices."""
        return [f"{row.value}_{option.value}" for row in self.rows for option in self.options]


class CompositeField(FormField):
    """A composite field that contains multiple other fields."""

    type: Literal["composite"]
    fields: list[InputField | ChoiceField]


class Fieldset(BaseModel):
    """A fieldset in a form."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    fields: list[InputField | ChoiceField | GridField | CompositeField]
    legend: Translation | None = None
    description: Translation | None = None
    rule: Rule | None = None

    def is_visible_for(self, data: dict) -> bool:
        """Given a data dict, check if this fieldset should be visible."""
        if self.rule and self.rule.type == "equals":
            return data[self.rule.field] == self.rule.value
        return True


class CustomForm(BaseModel):
    """A custom form."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    title: Translation | None = None
    task_cta: Translation | None = None
    description: Translation | None = None
    fieldsets: list[Fieldset]

    @field_validator("fieldsets")
    def validate_fieldsets(cls, v):
        """Validate fieldsets checking for duplicate field codes."""
        codes = set()
        for fieldset in v:
            for field in fieldset.fields:
                if field.code in codes:
                    raise ValueError(f"Duplicate field code `{field.code}`")
                codes.add(field.code)
        return v

    def get_fields(self) -> Generator[FormField, None, None]:
        """Get all fields in this form."""
        for fieldset in self.fieldsets:
            yield from fieldset.fields


def validate_form_definition(definition: dict) -> CustomForm:
    """Validate a form definition."""
    try:
        return CustomForm(**definition)
    except (TypeError, ValidationError) as exc:
        raise ValueError(exc) from exc


def validate_form_response(form_definition: dict, data: dict) -> dict:
    """Validate form data against a form definition."""
    form = validate_form_definition(form_definition)
    fields = []
    field_codes = set()

    if not isinstance(data, dict):
        raise ValueError("Response data should be a dict")

    for fieldset in form.fieldsets:
        if not fieldset.is_visible_for(data):
            continue
        for field in fieldset.fields:
            fields.append(field)
            field_codes.add(field.code)
            if type(field) is ChoiceField and field.other_option:
                field_codes.add(f"{field.code}__{field.other_option}")
            if field.required and (field.code not in data or not data[field.code]):
                raise ValueError(f"Missing required field `{field.code}`")

    for field in data:
        if field not in field_codes:
            raise ValueError(f"Unknown field `{field}`")

    for field in fields:
        if field.type == "composite":
            for subfield in field.fields:
                _validate_field(subfield, data)
        else:
            _validate_field(field, data)

    # clean data for XSS attacks
    # users normally shouldn't be able to enter HTML, but we can't be sure
    # TODO: if we expect HTML, we should create a valid field type for it

    return _sanitize_html(data)


def _validate_field(field: FormField, data: dict) -> None:
    """Validate fields checking for duplicate field codes."""
    if field.type in {"select", "option_group"} and field.code in data:
        options = {option.value for option in field.options}

        if field.multiple:
            _validate_options(options, data, field.code)
        else:
            if data[field.code] and data[field.code] not in options:
                raise ValueError(f"Invalid value `{data[field.code]}` for field `{field.code}`")

        if field.other_option and field.other_option in data[field.code]:
            other_code = f"{field.code}__{field.other_option}"
            if other_code not in data or not isinstance(data[other_code], str):
                raise ValueError(f"Field `{field.code}__{field.other_option}` should be defined, as a string")

    elif field.type in {"option_grid"} and field.multiple and field.code in data:
        _validate_options(set(field.all_options), data, field.code)

    elif field.type in {"option_grid"} and not field.multiple and field.code in data:
        if field.required and not data[field.code]:
            raise ValueError(f"Missing value for field `{field.code}`")

        if field.required and data[field.code] and not isinstance(data[field.code], dict):
            raise ValueError(f"Field `{field.code}` should be a dict")

        if field.required:
            options = {option.value for option in field.options}

            for row in field.rows:
                if not data[field.code][row.value] or data[field.code][row.value] not in options:
                    raise ValueError(
                        f"Invalid value `{data[field.code][row.value]}` for field " f"`{field.code}` > `{row.value}`"
                    )

    elif field.code in data:
        if not isinstance(data[field.code], str):
            raise ValueError(f"Field `{field.code}` should be a string")


def _validate_options(available_options: set[str], data: dict, field_code: str) -> None:
    """Validate options checking for duplicate option values."""
    if not isinstance(data[field_code], list):
        raise ValueError(f"Field `{field_code}` should be a list")

    for value in data[field_code]:
        if value not in available_options:
            raise ValueError(f"Invalid value `{data[field_code]}` for field `{field_code}`")

    if len(set(data[field_code])) != len(data[field_code]):
        raise ValueError(f"Duplicate values for field `{field_code}`")


def _sanitize_html(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = sanitize(value)
        if isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, str):
                    data[key][i] = sanitize(item)
        if isinstance(value, dict):
            data[key] = _sanitize_html(value)
    return data
