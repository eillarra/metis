import pytest

from metis.services.configurator import validate_education_configuration


@pytest.mark.parametrize(
    "config",
    [
        True,
        {"unknown_key": "unknown_value"},
        {"project_text_types": ["one", "two", "three"]},
        {
            "project_text_types": [
                {
                    "code": "one",
                    "name_nl": "Een",
                    "name_en": "One",
                }
            ]
        },
        {
            "project_text_types": [
                {
                    "code": "project.internship_agreement",
                },
                {
                    "code": "project.privacy_agreement",
                },
            ]
        },
        {
            "unknown_key": "unknown_value",
            "project_text_types": [
                {
                    "code": "project.internship_agreement",
                    "name": {"nl": "Stageovereenkomst", "en": "Internship agreement"},
                },
                {
                    "code": "project.privacy_agreement",
                    "name": {"nl": "Privacy verklaring", "en": "Privacy agreement"},
                },
            ],
        },
    ],
)
def test_config_is_invalid(config):
    with pytest.raises(ValueError):
        validate_education_configuration(config)


@pytest.mark.parametrize(
    "config",
    [
        {
            "project_text_types": [
                {
                    "code": "project.internship_agreement",
                    "title": {"nl": "Stageovereenkomst", "en": "Internship agreement"},
                },
                {
                    "code": "project.privacy_agreement",
                    "title": {"nl": "Privacy verklaring", "en": "Privacy agreement"},
                },
            ]
        },
    ],
)
def test_config_valid(config):
    validate_education_configuration(config)
