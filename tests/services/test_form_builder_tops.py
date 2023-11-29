import pytest

from metis.services.form_builder.tops import validate_tops_form_definition, validate_tops_form_response
from metis.utils.factories import ProjectFactory, ProjectPlaceFactory


@pytest.fixture
def project(db):
    """Return a project."""
    project = ProjectFactory()
    for _ in range(5):
        ProjectPlaceFactory(project=project)
    return project


@pytest.fixture
def form_definition():
    """Return a form definition for tops."""
    return {
        "type": "project_places",
        "num_tops": 5,
    }


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
    ],
)
@pytest.mark.unit
def test_definition_is_invalid(definition):
    """Test that an invalid form definition raises a ValueError."""
    with pytest.raises(ValueError):
        validate_tops_form_definition(definition)


@pytest.mark.parametrize(
    "definition",
    [
        {"type": "project_places", "num_tops": 10},
        {"type": "regions", "num_tops": 3},
    ],
)
@pytest.mark.unit
def test_definition_valid(definition):
    """Test that a valid form definition doesn't raise an exception."""
    validate_tops_form_definition(definition)


@pytest.mark.parametrize(
    "data, require_motivation",
    [
        (True, False),
        ({"unknown_key": "unknown_value"}, False),
        ({"tops": None}, False),
        ({"tops": []}, False),
        ({"tops": [1, 2, 3, 4]}, False),
        ({"tops": [1, 2, 3, 4, 5, 6]}, False),
        ({"tops": [1, 2, 3, 4, 4]}, False),
        ({"tops": [1, 2, 3, 4, 999]}, False),
        ({"tops": [1, 2, 3, 4, 5], "motivation": "motivation"}, True),
        ({"tops": [1, 2, 3, 4, 5], "motivation": {"1": "M1"}}, True),
        ({"tops": [1, 2, 3, 4, 5], "motivation": {"1": "M1", "2": "M2", "3": "M3", "4": "M4", "5": None}}, True),
        ({"tops": [1, 2, 3, 4, 5], "motivation": {"1": "M1", "2": "M2", "3": "M3", "4": "M4", "5": ["invalid"]}}, True),
    ],
)
@pytest.mark.unit
def test_response_is_invalid(project, form_definition, data, require_motivation):
    """Test that an invalid form response raises a ValueError."""
    with pytest.raises(ValueError):
        validate_tops_form_response({**form_definition, **{"require_motivation": require_motivation}}, data, project)


@pytest.mark.parametrize(
    "data, require_motivation",
    [
        ({"tops": [1, 2, 3, 4, 5]}, False),
        ({"tops": [1, 2, 3, 4, 5], "motivation": {"1": "M1", "2": "M2", "3": "M3", "4": "M4", "5": "M5"}}, True),
    ],
)
@pytest.mark.unit
def test_response_is_valid(project, form_definition, data, require_motivation):
    """Test that a valid form response doesn't raise an exception."""
    validate_tops_form_response({**form_definition, **{"require_motivation": require_motivation}}, data, project)
