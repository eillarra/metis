from metis.services.form_builder.custom_forms import CustomForm


def form_to_markdown(form_definition: dict, response: dict) -> str:
    """
    Given a form definition and some data, create a markdown representation of the data.
    """

    form = CustomForm(**form_definition)
    question_n = 0

    md = ""

    for fieldset in form.fieldsets:
        for field in fieldset.fields:
            question_n += 1

            if field.code in response and response[field.code]:
                md += f"#### {question_n}. {field.label.nl}\n\n"
                if field.type == "textarea":
                    md += response[field.code] + "\n"
                elif field.type == "text":
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
                    for option in field.options:
                        cols = []
                        for col in field.columns:
                            if f"{option.value}_{col.value}" in response[field.code]:
                                cols.append(col.label.nl)
                        if cols:
                            md += f"  - {option.label.nl}: {', '.join(cols)}\n"

                md += "\n"

    return md
