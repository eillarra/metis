import os
from http import HTTPStatus as status

from rest_framework.decorators import api_view
from rest_framework.response import Response

from metis.services.mailer.automate import parse_bouncing_email
from metis.services.mailer.base import schedule_email
from metis.services.mailer.contacts import schedule_bouncing_email_notice


@api_view(["post"])
def process_bouncing_email(request) -> Response:
    """Process an email from Outlook to mark emails as undeliverable."""
    power_automate_header = request.headers.get("x-powerautomate", None)

    if not power_automate_header or power_automate_header != os.getenv("POWER_AUTOMATE_HEADER"):
        return Response(status=status.BAD_REQUEST)

    email_body = request.body
    bouncing_email = parse_bouncing_email(email_body)

    if not bouncing_email:
        schedule_email(
            to=["helpdesk.metis@ugent.be"],
            subject="Metis API: Undeliverable email",
            text_content=email_body,
            tags=["type:undeliverable.email"],
        )
    else:
        schedule_bouncing_email_notice(bouncing_email)

    return Response(status=status.OK)
