from django.utils.html import conditional_escape
from pydantic import ValidationError
from typing import TYPE_CHECKING

from .custom_forms import CustomForm, ChoiceField
from .tops import TopsForm

if TYPE_CHECKING:
    from metis.models.stages.projects import Project


def escape_html(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = conditional_escape(value)
        if isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, str):
                    data[key][i] = conditional_escape(item)
        if isinstance(value, dict):
            data[key] = escape_html(value)
    return data


def fieldset_is_visible(fieldset, data: dict) -> bool:
    if fieldset.rule:
        if fieldset.rule.type == "equals":
            return data[fieldset.rule.field] == fieldset.rule.value
    return True


def validate_form_definition(definition: dict) -> CustomForm:
    """
    Validate a form definition.
    """

    try:
        return CustomForm(**definition)
    except (TypeError, ValidationError) as e:
        raise ValueError(e)


def validate_form_response(form_definition: dict, data: dict) -> dict:
    """
    Validate form data against a form definition.
    """

    form = validate_form_definition(form_definition)
    fields = []
    field_codes = set()

    if not isinstance(data, dict):
        raise ValueError("Data should be a dict")

    for fieldset in form.fieldsets:
        if not fieldset_is_visible(fieldset, data):
            continue
        for field in fieldset.fields:
            fields.append(field)
            field_codes.add(field.code)
            if type(field) is ChoiceField and field.other_option:
                field_codes.add(f"{field.code}__{field.other_option}")
            if field.required:
                if field.code not in data or not data[field.code]:
                    raise ValueError(f"Missing required field `{field.code}`")

    for field in data:
        if field not in field_codes:
            raise ValueError(f"Unknown field `{field}`")

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
                if data[field.code] and data[field.code] not in options:
                    raise ValueError(f"Invalid value `{data[field.code]}` for field `{field.code}`")

            if field.other_option and field.other_option in data[field.code]:
                other_code = f"{field.code}__{field.other_option}"
                if other_code not in data or not isinstance(data[other_code], str):
                    raise ValueError(f"Field `{field.code}__{field.other_option}` should be defined, as a string")

        elif field.type in {"option_grid"} and field.code in data:
            all_options = set()
            for option in field.options:
                for column in field.columns:
                    all_options.add(f"{option.value}_{column.value}")

            for value in data[field.code]:
                if value not in all_options:
                    raise ValueError(f"Invalid value `{data[field.code]}` for field `{field.code}`")

            if not isinstance(data[field.code], list):
                raise ValueError(f"Field `{field.code}` should be a list")

        elif field.code in data:
            if not isinstance(data[field.code], str):
                raise ValueError(f"Field `{field.code}` should be a string")

    # clean data for XSS attacks
    # users normally shouldn't be able to enter HTML, but we can't be sure
    # TODO: if we expect HTML, we should create a valid field type for it

    return escape_html(data)


def validate_tops_form_definition(definition: dict) -> TopsForm:
    """
    Validate a tops form definition.
    """

    try:
        return TopsForm(**definition)
    except (TypeError, ValidationError) as e:
        raise ValueError(e)


def validate_tops_form_response(form_definition: dict, data: dict, project: "Project") -> dict:
    """
    Validate form data against a form definition.
    """

    form = validate_tops_form_definition(form_definition)

    if not isinstance(data, dict):
        raise ValueError("Data should be a dict")

    if not isinstance(data.get("tops"), list):
        raise ValueError("Data should contain a list of tops")

    if form.type == "project_places":
        project_place_ids = set(project.place_set.values_list("id", flat=True))
        for project_place_id in data["tops"]:
            if project_place_id not in project_place_ids:
                raise ValueError(f"Invalid ProjectPlace id `{project_place_id}`")
        if len(set(data["tops"])) != len(data["tops"]):
            raise ValueError("Duplicate ProjectPlace ids")

    elif form.type == "regions":
        raise NotImplementedError("Regions form not implemented")

    try:
        if len(data["tops"]) != form.num_tops:
            raise ValueError("Invalid number of tops")
    except AttributeError:
        raise ValueError("Missing required field `tops`")

    return data
