import pytest

from metis.services.form_builder.validators import validate_form_response
from metis.utils.fixtures.forms import get_audiology_place_form


@pytest.fixture
def form_definition():
    return get_audiology_place_form()


@pytest.mark.parametrize(
    "data,escaped_text",
    [
        (
            {"voorkennis": "<script>alert('XSS testing!')</script>", "uurroster": ["maandag_VM"]},
            "&lt;script&gt;alert(&#x27;XSS testing!&#x27;)&lt;/script&gt;",
        ),
        (
            {"voorkennis": "<b onmouseover=alert('XSS testing!')></b>", "uurroster": ["maandag_VM"]},
            "&lt;b onmouseover=alert(&#x27;XSS testing!&#x27;)&gt;&lt;/b&gt;",
        ),
    ],
)
def test_xss_escaped(form_definition, data, escaped_text):
    validated_data = validate_form_response(form_definition, data)
    assert validated_data["voorkennis"] == escaped_text
