from django.utils.timezone import now

from .form_to_pdf import form_to_pdf
from .pdfwrap import PdfWrap
from .pdfwrap.django import PdfResponse

from metis.models import ProjectPlace


class PdfReport:
    def get_pdf(self):
        raise NotImplementedError

    def get_response(self):
        data = self.get_pdf()
        response = PdfResponse(data, as_attachment=True, filename="report.pdf")
        return response


class ProjectPlaceInformationPdf(PdfReport):
    def __init__(self, period_id: int):
        self.period_id = period_id
        self.project_places = ProjectPlace.objects.filter(
            availability_set__period_id=period_id,
            availability_set__min__gt=0,
        ).order_by("place__name")

    def get_pdf(self) -> bytes:
        with PdfWrap() as pdf:
            pdf.add_footer(f"{now()}")
            form_definition = None

            for project_place in self.project_places:
                form_response = project_place.form_responses.filter(
                    form__code="project_place_information",
                ).first()

                pdf.add_paragraph(project_place.place.name, "h2")

                # addresses

                addresses = [address.full_address for address in project_place.place.addresses.all()]
                if addresses:
                    pdf.add_paragraph("<br />".join(addresses))

                # form response

                if form_response:
                    if not form_definition:
                        form_definition = form_response.form.definition

                    if form_response.updated_by:
                        email = form_response.updated_by.email.lower()
                        pdf.add_paragraph(
                            f"""
                            <br />
                            <strong>{form_response.updated_by.name}</strong>
                            &lt;<a href="mailto:{email}">{email}</a>&gt;<br />
                            Updated at: {form_response.updated_at}<br />
                        """
                        )
                    pdf.add_separator()
                    pdf.add_spacer()
                    pdf = form_to_pdf(form_definition, form_response.data, pdf)

                else:
                    pdf.add_separator()
                    pdf.add_spacer()
                    pdf.add_paragraph("(Geen extra informatie beschikbaar)")

                pdf.add_page_break()

            data = pdf.get_data()

        return data
