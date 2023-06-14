# flake8: noqa
# fmt: off


def get_audiologo_student_form() -> dict:
    return {
        "description": {
            "nl": "Vul hier je gegevens in.",
            "en": "Fill in your details here.",
        },
        "fieldsets": [
            {
                "fields": [
                    {
                        "type": "option_group",
                        "code": "stage",
                        "label": {"nl": "Bereikbaarheid", "en": "Accessibility"},
                        "multiple": True,
                        "options": [
                            {"value": "nl_wallonie", "label": {"nl": "Interesse in stage NL/Wallonie", "en": "Interest in internship NL/Wallonie"}},
                            {"value": "auto", "label": {"nl": "Beschikbaarheid auto", "en": "Availability car"}},
                            {"value": "frans", "label": {"nl": "Tweetalig en/of voldoende kennis Frans", "en": "Bilingual and/or sufficient knowledge of French"}},
                        ],
                    },
                    {
                        "type": "option_group",
                        "code": "statuut",
                        "label": {"nl": "Statuut", "en": "Status"},
                        "multiple": True,
                        "options": [
                            {"value": "bijzonder_statuut", "label": {"nl": "Bijzonder statuut", "en": "Special status"}},
                            {"value": "werkstudent", "label": {"nl": "Werkstudent", "en": "Working student"}},
                            {"value": "beursstudent", "label": {"nl": "Beursstudent", "en": "Scholarship student"}},
                        ],
                    },
                    {
                        "type": "text",
                        "code": "opmerkingen",
                        "label": {"nl": "Opmerkingen", "en": "Remarks"},
                    }
                ]
            }
        ],
    }
