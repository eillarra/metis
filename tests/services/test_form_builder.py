import pytest

from metis.services.form_builder.validators import validate_form_definition
from metis.utils.fixtures.forms import get_audiology_place_form, get_logopedics_place_form


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
def test_definition_is_invalid(definition):
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
def test_definition_valid(definition):
    validate_form_definition(definition)
