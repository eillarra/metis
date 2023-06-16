# flake8: noqa
# fmt: off


def get_audiology_place_form() -> dict:
    return {
        "description": {
            "nl": "Vul hier de gegevens van de plaats in.",
            "en": "Fill in the details of the place here.",
        },
        "fieldsets": [
            {
                "legend": {"nl": "Stageinformatie", "en": "Internship information"},
                "fields": [
                    {
                        "type": "text",
                        "code": "voorkennis",
                        "label": {"nl": "Specifieke voorkennis vereist?", "en": "Specific prior knowledge required?"},
                    },
                    {
                        "type": "option_group",
                        "code": "patientenpopulatie",
                        "label": {"nl": "Patientenpopulatie", "en": "Patient population"},
                        "multiple": True,
                        "options": [
                            {"value": "neonaten_babys", "label": {"nl": "Neonaten / Baby's", "en": "Neonates / Babies"}},
                            {"value": "peuters_kleuters", "label": {"nl": "Peuters / Kleuters", "en": "Toddlers / Preschoolers"}},
                            {"value": "kinderen", "label": {"nl": "Kinderen (6-12 jaar)", "en": "Children (6-12)"}},
                            {"value": "adolescenten", "label": {"nl": "Adolescenten (13-17 jaar)", "en": "Teenagers (13-17)"}},
                            {"value": "volwassenen", "label": {"nl": "Volwassenen (>18 jaar)", "en": "Adults (>18)"}},
                        ],
                    },
                    {
                        "type": "option_group",
                        "code": "klinische_activiteiten",
                        "label": {"nl": "Klinische activiteiten", "en": "Clinical activities"},
                        "multiple": True,
                        "collapsed": True,
                        "options": [
                            {"value": "otoadmittantiemetrie", "label": {"nl": "Oto-admittantiemetrie", "en": "Otoacoustic emissions"}},
                            {"value": "tonale_audiometrie", "label": {"nl": "Tonale audiometrie", "en": "Tonal audiometry"}},
                            {"value": "vocale_audiometrie", "label": {"nl": "Vocale audiometrie", "en": "Vocal audiometry"}},
                            {"value": "kinderaudiometrie", "label": {"nl": "Kinderaudiometrie", "en": "Pediatric audiometry"}},
                            {"value": "oaes", "label": {"nl": "OAE's", "en": "OAE's"}},
                            {"value": "aep", "label": {"nl": "AEP (BERA / ASSR / EcochG)", "en": "AEP (BERA / ASSR / EcochG)"}},
                            {"value": "vestibulair", "label": {"nl": "Vestibulair onderzoek (ENG / VNG / VEMP)", "en": "Vestibular examination (ENG / VNG / VEMP)"}},
                            {"value": "tinnitus", "label": {"nl": "Tinnitusmeting (diagnostiek / behandeling / TRT)", "en": "Tinnitus measurement (diagnostics / treatment / TRT)"}},
                            {"value": "stemvorkproeven", "label": {"nl": "Stemvorkproeven", "en": "Tuning fork tests"}},
                            {"value": "other", "label": {"nl": "Andere", "en": "Other"}},
                        ],
                        "other_option": "other",
                    },
                    {
                        "type": "option_group",
                        "code": "prothetische_activiteiten",
                        "label": {"nl": "Prothetische activiteiten", "en": "Prosthetic activities"},
                        "multiple": True,
                        "collapsed": True,
                        "options": [
                            {"value": "tonale_audiometrie", "label": {"nl": "Tonale audiometrie", "en": "Tonal audiometry"}},
                            {"value": "vocale_audiometrie", "label": {"nl": "Vocale audiometrie", "en": "Vocal audiometry"}},
                            {"value": "hoortoestelaanpassing", "label": {"nl": "Hoortoestelaanpassing", "en": "Hearing aid fitting"}},
                            {"value": "onderhoud", "label": {"nl": "Onderhoud hoortoestellen", "en": "Hearing aid maintenance"}},
                            {"value": "lokalisatietesten", "label": {"nl": "Lokalisatietesten", "en": "Localization tests"}},
                            {"value": "hoorhulpmiddelen", "label": {"nl": "Hoorhulpmiddelen", "en": "Hearing aids"}},
                            {"value": "baha", "label": {"nl": "BAHA", "en": "BAHA"}},
                            {"value": "lawaaibescherming", "label": {"nl": "Lawaaibescherming", "en": "Noise protection"}},
                            {"value": "tinnitus", "label": {"nl": "Tinnitusmeting (diagnostiek / behandeling / TRT)", "en": "Tinnitus measurement (diagnostics / treatment / TRT)"}},
                            {"value": "zwemdoppen", "label": {"nl": "Zwemdoppen", "en": "Swimming plugs"}},
                            {"value": "other", "label": {"nl": "Andere", "en": "Other"}},
                        ],
                        "other_option": "other",
                    },
                    {
                        "type": "option_group",
                        "code": "rehabilitatieve_activiteiten",
                        "label": {"nl": "Rehabilitatieve activiteiten", "en": "Rehabilitative activities"},
                        "multiple": True,
                        "collapsed": True,
                        "options": [
                            {"value": "ci_fitting", "label": {"nl": "CI-fitting", "en": "CI fitting"}},
                            {"value": "hoortraining", "label": {"nl": "Hoortraining", "en": "Hearing training"}},
                            {"value": "lipleestraining", "label": {"nl": "Lipleestraining", "en": "Lip reading training"}},
                        ],
                    },
                    {
                        "type": "text",
                        "code": "andere_activiteiten",
                        "label": {"nl": "Andere audiologische activiteiten", "en": "Other audiological activities"},
                    }
                ]
            },
            {
                "legend": {"nl": "Praktische informatie", "en": "Practical information"},
                "fields": [
                    {
                        "type": "timetable",
                        "code": "uurroster",
                        "label": {"nl": "Uurrooster", "en": "Timetable"},
                        "days": ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag"],
                        "required": True
                    },
                    {
                        "type": "option_group",
                        "code": "kleding",
                        "label": {"nl": "Kleding en professioneel voorkomen", "en": "Clothing and professional appearance"},
                        "multiple": True,
                        "options": [
                            {"value": "neutral", "label": {"nl": "Nette neutrale kledij", "en": "Neat neutral clothing"}},
                            {"value": "white_scrubs", "label": {"nl": "Witte schort", "en": "White scrubs"}},
                            {"value": "badge", "label": {"nl": "Badge 'audioloog in opleiding' verplicht", "en": "Badge 'audioloog in opleiding' required"}},
                            {"value": "no_signs", "label": {"nl": "Geen uiterlijke tekenen van religieuze, politieke of levensbeschouwelijke aard", "en": "No outward signs of religious, political or philosophical nature"}},
                            {"value": "other", "label": {"nl": "Andere", "en": "Other"}},
                        ],
                        "other_option": "other",
                    },
                    {
                        "type": "option_group",
                        "code": "bereikbaarheid",
                        "label": {"nl": "Bereikbaarheid stageplaats", "en": "Accessibility of internship location"},
                        "options": [
                            {"value": "makkelijk_bereikbaar", "label": {"nl": "Makkelijk bereikbaar met openbaar vervoer", "en": "Easily accessible by public transport"}},
                            {"value": "moeilijk_bereikbaar", "label": {"nl": "Moeilijk bereikbaar met openbaar vervoer", "en": "Difficult to reach by public transport"}},
                            {"value": "auto_gewenst", "label": {"nl": "Eigen auto gewenst", "en": "Own car desired"}},
                            {"value": "auto_noodzakelijk", "label": {"nl": "Eigen auto noodzakelijk", "en": "Own car required"}},
                            {"value": "fiets", "label": {"nl": "Fiets voorzien", "en": "Bicycle provided"}},
                        ],
                    },
                    {
                        "type": "text",
                        "code": "treinstation",
                        "label": {"nl": "Plaats en afstand tot dichtstbijzijnde treinstation", "en": "Location and distance to nearest train station"},
                    },
                    {
                        "type": "text",
                        "code": "verblijf",
                        "label": {"nl": "Mogelijkheden tot verblijf", "en": "Accommodation options"},
                    },
                    {
                        "type": "text",
                        "code": "andere",
                        "label": {"nl": "Andere relevante info betreffende stageplaats, populatie...", "en": "Other relevant information regarding internship location, population..."},
                    }
                ]
            }
        ],
    }


def get_logopedics_place_form() -> dict:
    return {
        "description": {
            "nl": "Vul hier de gegevens van de plaats in.",
            "en": "Fill in the details of the place here.",
        },
        "fieldsets": [
            {
                "legend": {"nl": "Stageinformatie", "en": "Internship information"},
                "fields": [
                    {
                        "type": "text",
                        "code": "voorkennis",
                        "label": {"nl": "Specifiek vereiste voorkennis / bijzondere interesse in", "en": "Specific required prior knowledge / special interest in"},
                    },
                    {
                        "type": "option_group",
                        "code": "patientenpopulatie",
                        "label": {"nl": "Patientenpopulatie", "en": "Patient population"},
                        "multiple": True,
                        "options": [
                            {"value": "neonaten_babys", "label": {"nl": "Neonaten / Baby's", "en": "Neonates / Babies"}},
                            {"value": "peuters_kleuters", "label": {"nl": "Peuters / Kleuters", "en": "Toddlers / Preschoolers"}},
                            {"value": "kinderen", "label": {"nl": "Kinderen (6-12 jaar)", "en": "Children (6-12)"}},
                            {"value": "adolescenten", "label": {"nl": "Adolescenten (13-17 jaar)", "en": "Teenagers (13-17)"}},
                            {"value": "volwassenen", "label": {"nl": "Volwassenen (>18 jaar)", "en": "Adults (>18)"}},
                        ],
                    },
                    {
                        "type": "option_group",
                        "code": "logopedische_activiteiten",
                        "label": {"nl": "Logopedische activiteiten", "en": "Speech therapy activities"},
                        "multiple": True,
                        "options": [
                            {"value": "therapeutisch", "label": {"nl": "(Hoofzakelijk) Therapeutische setting", "en": "(Mainly) Therapeutic setting"}},
                            {"value": "diagnostisch", "label": {"nl": "(Hoofzakelijk) Diagnostische setting", "en": "(Mainly) Diagnostic setting"}},
                            {"value": "observatie", "label": {"nl": "Observatie van andere disciplines mogelijk", "en": "Observation of other disciplines possible"}},
                        ],
                    },
                    {
                        "type": "option_group",
                        "code": "pathologieen",
                        "label": {"nl": "Pathologieën", "en": "Pathologies"},
                        "multiple": True,
                        "options": [
                            {"value": "mondgewoonten", "label": {"nl": "Afwijkende mondgewoonten", "en": "Abnormal oral habits"}},
                            {"value": "dysfagie", "label": {"nl": "Dysfagie", "en": "Dysphagia"}},
                            {"value": "gehoorstoornissen", "label": {"nl": "Gehoorstoornissen", "en": "Hearing disorders"}},
                            {"value": "lees_schrijf_rekenstoornissen", "label": {"nl": "Lees-, schrijf- en rekenstoornissen", "en": "Reading, writing and arithmetic disorders"}},
                            {"value": "neurogene_taalstoornissen", "label": {"nl": "Neurogene spraak- en taalstoornissen", "en": "Neurogenic speech and language disorders"}},
                            {"value": "ontwikkelingsdysfasie", "label": {"nl": "Ontwikkelingsdysfasie", "en": "Developmental dysphasia"}},
                            {"value": "schisis", "label": {"nl": "Schisis", "en": "Cleft lip and palate"}},
                            {"value": "taalontwikkelingsstoornissen", "label": {"nl": "Sparaak- en taalontwikkelingsstoornissen", "en": "Speech and language development disorders"}},
                            {"value": "stemstoornissen", "label": {"nl": "Stemstoornissen", "en": "Voice disorders"}},
                            {"value": "stotteren", "label": {"nl": "Stotteren", "en": "Stuttering"}},
                            {"value": "other", "label": {"nl": "Andere", "en": "Other"}},
                        ],
                        "other_option": "other",
                    },
                ]
            },
            {
                "legend": {"nl": "Praktische informatie", "en": "Practical information"},
                "fields": [
                    {
                        "type": "timetable",
                        "code": "uurroster",
                        "label": {"nl": "Uurrooster", "en": "Timetable"},
                        "days": ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag"],
                        "required": True
                    },
                    {
                        "type": "option_group",
                        "code": "kleding",
                        "label": {"nl": "Kleding en professioneel voorkomen", "en": "Clothing and professional appearance"},
                        "multiple": True,
                        "options": [
                            {"value": "neutral", "label": {"nl": "Nette neutrale kledij", "en": "Neat neutral clothing"}},
                            {"value": "white_scrubs", "label": {"nl": "Witte schort", "en": "White scrubs"}},
                            {"value": "badge", "label": {"nl": "Badge 'logopedist in opleiding' verplicht", "en": "Badge 'logopedist in opleiding' required"}},
                            {"value": "no_signs", "label": {"nl": "Geen uiterlijke tekenen van religieuze, politieke of levensbeschouwelijke aard", "en": "No outward signs of religious, political or philosophical nature"}},
                            {"value": "other", "label": {"nl": "Andere", "en": "Other"}},
                        ],
                        "other_option": "other",
                    },
                    {
                        "type": "option_group",
                        "code": "bereikbaarheid",
                        "label": {"nl": "Bereikbaarheid stageplaats", "en": "Accessibility of internship location"},
                        "options": [
                            {"value": "makkelijk_bereikbaar", "label": {"nl": "Makkelijk bereikbaar met openbaar vervoer", "en": "Easily accessible by public transport"}},
                            {"value": "moeilijk_bereikbaar", "label": {"nl": "Moeilijk bereikbaar met openbaar vervoer", "en": "Difficult to reach by public transport"}},
                            {"value": "auto_gewenst", "label": {"nl": "Eigen auto gewenst", "en": "Own car desired"}},
                            {"value": "auto_noodzakelijk", "label": {"nl": "Eigen auto noodzakelijk", "en": "Own car required"}},
                            {"value": "fiets", "label": {"nl": "Fiets voorzien", "en": "Bicycle provided"}},
                        ],
                    },
                    {
                        "type": "text",
                        "code": "treinstation",
                        "label": {"nl": "Plaats en afstand tot dichtstbijzijnde treinstation", "en": "Location and distance to nearest train station"},
                    },
                    {
                        "type": "text",
                        "code": "verblijf",
                        "label": {"nl": "Mogelijkheden tot verblijf", "en": "Accommodation options"},
                    },
                    {
                        "type": "text",
                        "code": "andere",
                        "label": {"nl": "Andere relevante info betreffende stageplaats, populatie...", "en": "Other relevant information regarding internship location, population..."},
                    }
                ]
            }
        ],
    }
