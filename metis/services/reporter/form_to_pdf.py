from metis.services.form_builder.custom_forms import CustomForm


def _add_text_response(pdf, field, response):
    pdf.add_paragraph(response[field.code])


def _add_textarea_response(pdf, field, response):
    text = response[field.code].replace("\n", "<br />")
    pdf.add_paragraph(text)


def _add_choice_response(pdf, field, response):
    li = []
    for option in field.options:
        responses = response[field.code] if field.multiple else [response[field.code]]
        if option.value in responses:
            text = option.label.nl
            if field.other_option and option.value == field.other_option:
                text += f': {response[f"{field.code}__{field.other_option}"]}'
            li.append(f"- {text}")
    pdf.add_paragraph("<br />".join(li))


def _add_grid_response(pdf, field, response):
    li = []
    for option in field.options:
        cols = []
        for col in field.columns:
            if f"{option.value}_{col.value}" in response[field.code]:
                cols.append(col.label.nl)
        if cols:
            li.append(f"- {option.label.nl}: {', '.join(cols)}")
    pdf.add_paragraph("<br />".join(li))


def form_to_pdf(form_definition: dict, response: dict, pdf):
    form = CustomForm(**form_definition)
    question_n = 0

    for fieldset in form.fieldsets:
        for field in fieldset.fields:
            question_n += 1

            if field.code in response and response[field.code]:
                pdf.add_paragraph(f"{question_n}. {field.label.nl}", "h6", keep_with_next=True)
                if field.type == "textarea":
                    _add_textarea_response(pdf, field, response)
                elif field.type == "text":
                    _add_text_response(pdf, field, response)
                elif field.type in {"select", "option_group"}:
                    _add_choice_response(pdf, field, response)
                elif field.type == "option_grid":
                    _add_grid_response(pdf, field, response)

    return pdf
