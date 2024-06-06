from typing import TYPE_CHECKING

from metis.services.form_builder.custom_forms import CustomForm
from metis.services.form_builder.tops import TopsForm


if TYPE_CHECKING:
    from metis.models.rel.forms import FormResponse


def custom_form_to_markdown(form_definition: dict, response: dict) -> str:
    """Given a form definition and some data, create a markdown representation of the data."""
    form = CustomForm(**form_definition)
    question_n = 0

    md = ""

    for fieldset in form.fieldsets:
        for field in fieldset.fields:
            question_n += 1

            if field.code in response and response[field.code]:
                md += f"#### {question_n}. {field.label.nl}\n\n"

                if field.type in {"text", "textarea", "number", "date", "email", "tel", "url"}:
                    md += response[field.code] + "\n"

                elif field.type in {"select", "option_group"}:
                    for option in field.options:
                        responses = response[field.code] if field.multiple else [response[field.code]]
                        if option.value in responses:
                            text = option.label.nl
                            if field.other_option and option.value == field.other_option:
                                text += f': {response[f"{field.code}__{field.other_option}"]}'
                            md += f"  - {text}\n"

                elif field.type == "option_grid":
                    for row in field.rows:
                        choices = []

                        for option in field.options:
                            if f"{row.value}_{option.value}" in response[field.code]:
                                choices.append(option.label.nl)

                        if row.value in response[field.code]:
                            option = next(
                                (o for o in field.options if o.value == response[field.code][row.value]), None
                            )

                            if option:
                                choices.append(option.label.nl)

                        if responses:
                            md += f"  - {row.label.nl}: {', '.join(choices)}\n"

                md += "\n"

    return md


def tops_form_to_markdown(form_definition: dict, response: dict, project_places: list) -> str:
    project_places_by_id = {place.id: place for place in project_places}
    form = TopsForm(**form_definition)

    md = ""

    if not response["tops"]:
        return "No tops selected."

    for idx, project_place_id in enumerate(response["tops"]):
        if project_place_id in project_places_by_id:
            place = project_places_by_id[project_place_id].place
            if form.require_motivation:
                md += f'<p class="keep-with-next q-ma-none">{idx + 1}. {place}</p>'
                md += f'<p class="text-body2 q-ma-none">{response["motivation"][str(project_place_id)]}</p>'
                md += '<pdf:spacer height="15" />'
            else:
                md += f"{idx + 1}. {place}\n"

    return md


def response_to_markdown(response: "FormResponse"):
    if response.questioning.type == response.questioning.STUDENT_TOPS:
        questioning = response.questioning
        return tops_form_to_markdown(
            questioning.form_definition, response.data, questioning.get_support_data()["project_places"]
        )

    return custom_form_to_markdown(response.questioning.form_definition, response.data)
