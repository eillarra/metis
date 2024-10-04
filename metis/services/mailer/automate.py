import re


def parse_bouncing_email(body: str) -> str | None:
    """Parse the email address from a postmaster bouncing email body.

    :param body: The body of the email.
    :return: The email address that is bouncing.
    """
    original_message_headers = False
    email = None

    for line in body.split("\n"):
        line = line.strip().lower()

        if original_message_headers:
            if line.startswith("to:") or ("to:" in line and "reply-to:" not in line):
                email = line.split("to:")[1].strip()
                break

            elif "recipient address:" in line:
                email = line.split("recipient address:")[1].strip()
                break

        elif "original message headers" in line or "oorspronkelijke berichtkoppen" in line:
            original_message_headers = True

    if email:
        email = re.search(r"[\w\.-]+@[\w\.-]+", email)
        return email.group() if email else None

    return None
