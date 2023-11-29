import pytest

from metis.services.form_builder.custom_forms import validate_form_definition, validate_form_response
from metis.utils.fixtures.forms import get_audiology_place_form, get_logopedics_place_form


@pytest.fixture
def form_definition():
    """Return a form definition for the audiology place form."""
    return get_audiology_place_form()


@pytest.mark.parametrize(
    "definition",
    [
        True,
        {"unknown_key": "unknown_value"},
        {
            "fieldsets": [
                {
                    "fields": [
                        {
                            "type": "text",
                            "code": "first_name",
                            "label": "invalid label",
                            "required": True,
                        },
                    ],
                },
            ]
        },
        {
            "fieldsets": [
                {
                    "fields": [
                        {
                            "type": "invalid_type",
                            "code": "first_name",
                            "label": {"nl": "Voornaam", "en": "First name"},
                            "required": True,
                        },
                    ],
                },
            ]
        },
        {
            "fieldsets": [
                {
                    "fields": [
                        {
                            "type": "text",
                            "code": "duplicate_code",
                            "label": {"nl": "Voornaam", "en": "First name"},
                            "required": True,
                        },
                        {
                            "type": "text",
                            "code": "duplicate_code",
                            "label": {"nl": "Acternaam", "en": "Last name"},
                        },
                    ],
                },
            ]
        },
        {
            "fieldsets": [
                {
                    "fields": [
                        {
                            "type": "select",
                            "code": "colors",
                            "label": {"nl": "Kleuren", "en": "Colors"},
                            "options": [
                                {"value": "red", "label": {"nl": "Rood", "en": "Red"}},
                                {"value": "red", "label": {"nl": "Groen", "en": "Green"}},
                            ],
                        },
                    ],
                },
            ]
        },
        {
            "fieldsets": [
                {
                    "fields": [
                        {
                            "type": "text",
                            "code": "colors",
                            "multiple": True,
                            "options": [
                                {"value": 1, "label": {"nl": "Rood", "en": "Red"}},
                                {"value": 2, "label": {"nl": "Groen", "en": "Green"}},
                            ],
                        },
                    ],
                },
            ]
        },
    ],
)
@pytest.mark.unit
def test_definition_is_invalid(definition):
    """Test that an invalid form definition raises a ValueError."""
    with pytest.raises(ValueError):
        validate_form_definition(definition)


@pytest.mark.parametrize(
    "definition",
    [
        {
            "fieldsets": [
                {
                    "fields": [
                        {
                            "type": "text",
                            "code": "first_name",
                            "label": {"nl": "Voornaam", "en": "First name"},
                            "required": True,
                        },
                    ],
                },
            ]
        },
        get_audiology_place_form(),
        get_logopedics_place_form(),
    ],
)
@pytest.mark.unit
def test_definition_valid(definition):
    """Test that a valid form definition doesn't raise an exception."""
    validate_form_definition(definition)


@pytest.mark.parametrize(
    "definition",
    [
        {
            "fieldsets": [
                {
                    "fields": [
                        {
                            "type": "text",
                            "code": "first_name",
                            "label": {"nl": "Voornaam", "en": "First name"},
                            "required": True,
                        },
                    ],
                },
            ]
        },
    ],
)
@pytest.mark.unit
def test_get_fields(definition):
    """Test that a valid form definition doesn't raise an exception."""
    form = validate_form_definition(definition)
    assert list(form.get_fields()) == list(form.fieldsets[0].fields)


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
        {"uurroster": ["maandag_VM"], "klinische_activiteiten": ["oaes", "oaes"]},
        {"uurroster": ["maandag_VM"], "bereikbaarheid": "unknown_value"},
        {"uurroster": ["maandag_VM", "maandag_VM"]},
        {"uurroster": "maandag_VM"},
        {"uurroster": ["maandag_VM"], "unknown_key": "unknown_value"},
        {"uurroster": ["maandag_VM"], "voorkennis": ["not_a_string"]},
    ],
)
@pytest.mark.unit
def test_response_is_invalid(form_definition, data):
    """Test that an invalid form response raises a ValueError."""
    with pytest.raises(ValueError):
        validate_form_response(form_definition, data)


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
@pytest.mark.unit
def test_response_is_valid(form_definition, data):
    """Test that a valid form response doesn't raise an exception."""
    validate_form_response(form_definition, data)
