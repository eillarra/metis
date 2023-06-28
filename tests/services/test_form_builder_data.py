import pytest

from metis.services.form_builder.validators import validate_custom_form_data
from metis.utils.fixtures.forms import get_audiology_place_form


@pytest.fixture
def form_definition():
    return get_audiology_place_form()


@pytest.mark.parametrize(
    "data",
    [
        True,
        {"unknown_key": "unknown_value"},
        {"klinische_activiteiten": "not_a_list"},
        {"klinische_activiteiten": ["oaes", "unknown_value"]},
        {"bereikbaarheid": ["not_multiple"]},
        {"uurroster": "required_but_list"},
        {"uurroster": []},
        {"uurroster": ["required_and_valid_value"]},
        # the next one is valid, but we still miss the required field "uurroster"
        {"klinische_activiteiten": ["oaes", "aep"]},
        # if other is selected, we need to set a value
        {"uurroster": ["maandag_VM"], "klinische_activiteiten": ["oaes", "aep", "other"]},
        # and it should be a list, when choice is multiple
        {"uurroster": ["maandag_VM"], "klinische_activiteiten": "oaes"},
        # and a valid option
        {"uurroster": ["maandag_VM"], "klinische_activiteiten": ["oaes", "unknown_value"]},
        {"uurroster": ["maandag_VM"], "bereikbaarheid": "unknown_value"},
    ],
)
def test_definition_is_invalid(form_definition, data):
    with pytest.raises(ValueError):
        validate_custom_form_data(form_definition, data)


@pytest.mark.parametrize(
    "data",
    [
        {"uurroster": ["maandag_VM"]},
        {
            "uurroster": ["maandag_VM"],
            "klinische_activiteiten": ["oaes", "aep", "other"],
            "klinische_activiteiten__other": "some value",
        },
    ],
)
def test_definition_is_valid(form_definition, data):
    validate_custom_form_data(form_definition, data)
