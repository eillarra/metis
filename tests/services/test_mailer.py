import pytest

from metis.services.mailer import clean_shared_email


@pytest.mark.parametrize(
    "fake_email,email",
    [
        ("info++asterix@comic.com", "info@comic.com"),
        ("info++obelix@comic.com", "info@comic.com"),
        ("info++panoramix@comic.com", "info@comic.com"),
    ],
)
def test_clean_shared_email(fake_email, email):
    """Test that the shared email is cleaned."""
    assert clean_shared_email(fake_email) == email
