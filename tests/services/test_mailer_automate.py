from pathlib import Path

import pytest

from metis.services.mailer.automate import parse_bouncing_email


@pytest.mark.parametrize(
    "filename,bouncing_email",
    [
        ("microsoft_undeliverable.txt", "asterix@comic.com"),
        ("postmaster_onbestelbaar.txt", "obelix@comic.com"),
        ("postmaster_undeliverable.txt", "panoramix@comic.com"),
    ],
)
def test_parse_bouncing_email(filename, bouncing_email):
    """Test that the email address is extracted from a postmaster bouncing email body."""
    parent_dir = Path(__file__).resolve().parent

    with open(parent_dir / "automate_data" / filename) as f:
        body = f.read()
        assert parse_bouncing_email(body) == bouncing_email
