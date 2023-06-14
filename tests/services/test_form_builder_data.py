import pytest

from metis.services.form_builder import validate_form_data
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
        {"openingsuren": ["required_but_string"]},
        # the next one is valid, but we still miss the required field "openingsuren"
        {"klinische_activiteiten": ["oaes", "aep"]},
        # if other is selected, we need to set a value
        {"openingsuren": "required", "klinische_activiteiten": ["oaes", "aep", "other"]},
        # and it should be a list, when choice is multiple
        {"openingsuren": "required", "klinische_activiteiten": "oaes"},
        # and a valid option
        {"openingsuren": "required", "klinische_activiteiten": ["oaes", "unknown_value"]},
        {"openingsuren": "required", "bereikbaarheid": "unknown_value"},
    ],
)
def test_definition_is_invalid(form_definition, data):
    with pytest.raises(ValueError):
        validate_form_data(form_definition, data)


@pytest.mark.parametrize(
    "data",
    [
        {"openingsuren": "only_one_required"},
        {
            "openingsuren": "required",
            "klinische_activiteiten": ["oaes", "aep", "other"],
            "klinische_activiteiten__other": "some value",
        },
    ],
)
def test_definition_is_valid(form_definition, data):
    validate_form_data(form_definition, data)
