

from ..form_builder import Form


def _add_text_response(pdf, field, response):
    pdf.add_paragraph(response[field.code])


def _add_choice_response(pdf, field, response):
    if field.multiple:
        responses = [f"- {option.label.nl}<br />" for option in field.options if option.value in response[field.code]]
        pdf.add_paragraph("".join(responses))
    else:
        for option in field.options:
            if option.value == response[field.code]:
                pdf.add_paragraph(f"- {option.label.nl}")
                break


def _add_grid_response(pdf, field, response):
    responses = []
    for option in field.options:
        cols = []
        for col in field.columns:
            if f"{option.value}_{col.value}" in response[field.code]:
                cols.append(col.label.nl)
        if cols:
            responses.append(f"- {option.label.nl}: {', '.join(cols)}<br />")
    pdf.add_paragraph("".join(responses))


def form_to_pdf(form_definition: dict, response: dict, pdf):
    form = Form(**form_definition)
    question_n = 0

    for fieldset in form.fieldsets:
        for field in fieldset.fields:
            question_n += 1

            if field.code in response and response[field.code]:
                pdf.add_paragraph(f"{question_n}. {field.label.nl}", "h6")
                if field.type == "text":
                    _add_text_response(pdf, field, response)
                elif field.type in {"select", "option_group"}:
                    _add_choice_response(pdf, field, response)
                elif field.type == "option_grid":
                    _add_grid_response(pdf, field, response)

    return pdf
