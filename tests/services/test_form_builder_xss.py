import pytest

from metis.services.form_builder.custom_forms import validate_form_response
from metis.utils.fixtures.forms import get_audiology_place_form


@pytest.fixture
def form_definition():
    """Return a form definition for the audiology place form."""
    return get_audiology_place_form()


@pytest.mark.parametrize(
    "data,escaped_text",
    [
        ({"voorkennis": "Test!<script>alert('XSS testing!')</script>", "uurroster": ["maandag_VM"]}, "Test!"),
        ({"voorkennis": "<b onmouseover=alert('XSS testing!')>Metis</b>", "uurroster": ["maandag_VM"]}, "Metis"),
    ],
)
def test_xss_escaped(form_definition, data, escaped_text):
    """Test that XSS is escaped."""
    validated_data = validate_form_response(form_definition, data)
    assert validated_data["voorkennis"] == escaped_text
