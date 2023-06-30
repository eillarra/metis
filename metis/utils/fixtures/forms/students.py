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
                        "type": "text",
                        "code": "rijksregisternummer",
                        "label": {"nl": "Rijksregisternummer", "en": "National register number"},
                        "mask": "##.##.##-###.##",
                    },
                    {
                        "type": "text",
                        "code": "gsm_nummer",
                        "label": {"nl": "GSM-nummer", "en": "Mobile phone number"},
                        "mask": "#### ## ## ##",
                    },
                    {
                        "type": "text",
                        "code": "adres",
                        "label": {"nl": "Adres", "en": "Address"},
                    },
                    {
                        "type": "text",
                        "code": "stad",
                        "label": {"nl": "Stad", "en": "City"},
                    },
                    {
                        "type": "text",
                        "code": "adres2",
                        "label": {
                            "nl": "Logeeradres elders in Belgie dat kan fungeren als uitvalsbasis tijdens stage",
                            "en": "Address elsewhere in Belgium that can serve as a base during internship",
                        },
                    },
                    {
                        "type": "text",
                        "code": "stad2",
                        "label": {"nl": "Stad 2", "en": "City 2"},
                    },
                    {
                        "type": "option_group",
                        "code": "kot_gent",
                        "label": {"nl": "Kot in Gent", "en": "Dorm in Gent"},
                        "options": [
                            {"value": "ja", "label": {"nl": "Ja", "en": "Yes"}},
                            {"value": "nee", "label": {"nl": "Nee", "en": "No"}},
                        ],
                    },
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
                        "other_option": "frans",
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
                        "type": "textarea",
                        "code": "opmerkingen",
                        "label": {"nl": "Opmerkingen", "en": "Remarks"},
                    }
                ]
            }
        ],
    }
