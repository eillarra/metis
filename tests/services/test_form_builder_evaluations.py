import pytest

from metis.services.form_builder.evaluations import (
    validate_evaluation_form_definition,
    validate_evaluation_form_response,
)


@pytest.fixture
def form_definition():
    """Return a evaluation form definition."""
    return {
        "scores": [
            {"value": None, "label": {"en": "n/a", "nl": "n.v.t."}, "points": None},
            {"value": "one", "label": {"en": "1", "nl": "1"}, "points": 1},
            {"value": "two", "label": {"en": "2", "nl": "2"}, "points": 2},
            {"value": "three", "label": {"en": "3", "nl": "3"}, "points": 3},
        ],
        "sections": [
            {
                "code": "one",
                "items": [
                    {"value": "1", "label": {"en": "Item 1", "nl": "Item 1"}},
                    {"value": "2", "label": {"en": "Item 2", "nl": "Item 2"}},
                    {"value": "3", "label": {"en": "Item 3", "nl": "Item 3"}},
                ],
            },
        ],
    }


@pytest.fixture
def form_definition_with_section_remarks(form_definition):
    """Return a evaluation form definition."""
    sections = form_definition["sections"]
    sections[0]["with_remarks"] = True
    return {**form_definition, **{"sections": sections}}


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
            "scores": [
                {"value": "one", "label": {"en": "n/a", "nl": "n.v.t."}, "points": None},
                {"value": "one", "label": {"en": "1", "nl": "1"}, "points": 1},
            ],
            "sections": [
                {
                    "code": "one",
                    "items": [
                        {"value": "1", "label": {"en": "Item 1", "nl": "Item 1"}},
                        {"value": "2", "label": {"en": "Item 2", "nl": "Item 2"}},
                    ],
                },
            ],
        },
        {
            "scores": [
                {"value": None, "label": {"en": "n/a", "nl": "n.v.t."}, "points": None},
                {"value": "one", "label": {"en": "1", "nl": "1"}, "points": None},
            ],
            "sections": [
                {
                    "code": "one",
                    "items": [
                        {"value": "1", "label": {"en": "Item 1", "nl": "Item 1"}},
                        {"value": "2", "label": {"en": "Item 2", "nl": "Item 2"}},
                    ],
                },
            ],
        },
        {
            "scores": [
                {"value": None, "label": {"en": "n/a", "nl": "n.v.t."}, "points": None},
                {"value": "one", "label": {"en": "1", "nl": "1"}, "points": 1},
            ],
            "sections": [],
        },
        {
            "scores": [],
            "sections": [
                {
                    "code": "one",
                    "items": [
                        {"value": "1", "label": {"en": "Item 1", "nl": "Item 1"}},
                        {"value": "2", "label": {"en": "Item 2", "nl": "Item 2"}},
                    ],
                },
            ],
        },
    ],
)
@pytest.mark.unit
def test_definition_is_invalid(definition):
    """Test that an invalid form definition raises a ValueError."""
    with pytest.raises(ValueError):
        validate_evaluation_form_definition(definition)


@pytest.mark.parametrize(
    "definition",
    [
        {
            "scores": [
                {"value": "one", "label": {"en": "1", "nl": "1"}, "points": 1},
                {"value": "two", "label": {"en": "2", "nl": "2"}, "points": 2},
            ],
            "sections": [
                {
                    "code": "one",
                    "items": [
                        {"value": "1", "label": {"en": "Item 1", "nl": "Item 1"}},
                    ],
                },
            ],
        },
    ],
)
@pytest.mark.unit
def test_definition_valid(definition):
    """Test that a valid form definition doesn't raise an exception."""
    validate_evaluation_form_definition(definition)


@pytest.mark.parametrize(
    "data",
    [
        True,
        {"global_score": "one", "global_remarks": "remarks", "unknown_key": "unknown_value"},
        {"global_score": "one", "global_remarks": "remarks", "tops": None},
        {"global_score": "one", "global_remarks": "remarks", "sections": None},
        {"global_score": "one", "global_remarks": "remarks", "sections": {"unknown": {}}},
        {"global_score": "one", "global_remarks": "remarks", "sections": {"one": None}},
        {"global_score": "one", "global_remarks": "remarks", "sections": {"one": {"scores": None}}},
        {"global_score": "one", "global_remarks": "remarks", "sections": {"one": {"scores": {"unknown": {}}}}},
        {"global_score": "one", "global_remarks": "remarks", "sections": {"one": {"scores": {"1": None}}}},
        {
            "global_score": "one",
            "sections": {"one": {"score": "one", "scores": {"1": ("one", None)}}},
        },
        {
            "global_score": "one",
            "global_remarks": None,
            "sections": {"one": {"score": "one", "scores": {"1": ("one", None)}}},
        },
        {
            "global_score": "unknown",
            "global_remarks": "remarks",
            "sections": {"one": {"score": "one", "scores": {"1": ("one", None)}}},
        },
    ],
)
@pytest.mark.unit
def test_response_is_invalid(form_definition, data):
    """Test that an invalid form response raises a ValueError."""
    with pytest.raises(ValueError):
        validate_evaluation_form_response(form_definition, data)


@pytest.mark.parametrize(
    "data",
    [
        {
            "global_score": "one",
            "global_remarks": "remarks",
            "sections": {"one": {"score": "one", "scores": {"1": ("one", None)}}},
        },
    ],
)
@pytest.mark.unit
def test_response_is_valid(form_definition, data):
    """Test that a valid form response doesn't raise an exception."""
    validate_evaluation_form_response(form_definition, data)


@pytest.mark.parametrize(
    "data",
    [
        {
            "global_score": "one",
            "global_remarks": "remarks",
            "sections": {"one": {"score": "one", "remarks": None, "scores": {"1": ("one", None)}}},
        },
    ],
)
@pytest.mark.unit
def test_response_with_remarks_is_invalid(form_definition_with_section_remarks, data):
    """Test that an invalid form response raises a ValueError (with section remarks)."""
    with pytest.raises(ValueError):
        validate_evaluation_form_response(form_definition_with_section_remarks, data)


@pytest.mark.parametrize(
    "data",
    [
        {
            "global_score": "one",
            "global_remarks": "remarks",
            "sections": {"one": {"score": "one", "remarks": "remarks", "scores": {"1": ("one", None)}}},
        },
    ],
)
@pytest.mark.unit
def test_response_with_remarks_is_valid(form_definition_with_section_remarks, data):
    """Test that a valid form response doesn't raise an exception (with section remarks)."""
    validate_evaluation_form_response(form_definition_with_section_remarks, data)
