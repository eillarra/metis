import pytest

from metis.utils.html import sanitize


@pytest.mark.parametrize(
    "text,escaped_text",
    [
        ("<script>alert('XSS testing!')</script>", ""),
        ("<b onmouseover=alert('XSS testing!')></b>", ""),
        ("metis'", "metis'"),
        ("“Metis”", "“Metis”"),
    ],
)
def test_sanitize(text, escaped_text):
    """Test that html is correctly sanitized, to avoid XSS atacks, but allow regular especial characters."""
    assert sanitize(text) == escaped_text
