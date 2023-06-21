from django.utils.timezone import now
from typing import TYPE_CHECKING

from metis.models.rel.forms import CustomFormResponse

from .form_to_pdf import form_to_pdf
from .pdfwrap import PdfWrap
from .pdfwrap.django import PdfResponse

if TYPE_CHECKING:
    from metis.models import ProjectPlace


class PdfReport:
    def get_pdf(self):
        raise NotImplementedError

    def get_response(self):
        data = self.get_pdf()
        response = PdfResponse(data, as_attachment=True, filename="report.pdf")
        return response


class ProjectPlaceInformationReport(PdfReport):
    def __init__(self, project_id: int):
        self.form_reponses = CustomFormResponse.objects.filter(
            form__project_id=project_id, form__code="project_place_information"
        ).prefetch_related("updated_by")

    def get_pdf(self) -> bytes:
        with PdfWrap() as pdf:
            pdf.add_footer(f"{now()}")

            form_definition = self.form_reponses[0].form.definition

            for form_response in self.form_reponses:
                if not form_response.content_object:
                    continue
                project_place: "ProjectPlace" = form_response.content_object

                pdf.add_paragraph(project_place.place.name, "h2")
                if form_response.updated_by:
                    pdf.add_paragraph(f"""
                        <strong>{form_response.updated_by.name}</strong>
                        &lt;<a href="mailto:{form_response.updated_by.email}">{form_response.updated_by.email}</a>&gt;<br />
                        Updated at: {form_response.updated_at}<br />
                    """
                    )
                pdf = form_to_pdf(form_definition, form_response.data, pdf)
                pdf.add_page_break()

            data = pdf.get_data()

        return data
