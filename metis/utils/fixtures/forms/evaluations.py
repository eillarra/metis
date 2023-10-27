# flake8: noqa
# fmt: off


description = {
    "nl": "Gelieve aan te duiden hoe de student voor de opgesomde deelaspecten scoort. Indien bepaalde aspecten (nog) niet aan bod kwamen gedurende de stage, dan worden deze aspecten niet gescoord. Gelieve bepaalde onderdelen met A en/of P te scoren om aan te geven of de student het onderdeel zelfstandig (Actief) kan uitvoeren, of de onderdelen nog observeert (Pasief). Met behulp van de deelscores en rekening houdend met de beoordelingscriteria komt u zo tot een algemene beoordeling, die uw globale indruk over de stage weergeeft. De student dient geslaagd te zijn op elk van de verschillende deelscores om voor de volledige stageperiode geslaagd te zijn.",
    "en": "Please indicate how the student scores for the listed sub-aspects. If certain aspects (still) did not come up during the internship, these aspects are not scored. Please score certain parts with A and / or P to indicate whether the student can perform the part independently (Active), or still observes the parts (Passive). Using the partial scores and taking into account the assessment criteria, you will arrive at an overall assessment, which reflects your overall impression of the internship. The student must have passed each of the different partial scores in order to pass the entire internship period.",
}


def get_audio_internship_evaluation_form_klinisch() -> dict:
    return {
        "description": description,
        "intermediate_evaluations": 1,
        "grades":[
            {"value": None, "label": {"nl": "n.v.t.", "en": "N/A"}},
            {"value": 1, "label": {"nl": "Onvoldoende", "en": "Insufficient"}},
            {"value": 3, "label": {"nl": "Net voldoende", "en": "Just sufficient"}},
            {"value": 5, "label": {"nl": "Voldoende", "en": "Sufficient"}},
            {"value": 6, "label": {"nl": "Goed", "en": "Good"}},
            {"value": 8, "label": {"nl": "Zeer goed", "en": "Very good"}},
            {"value": 9, "label": {"nl": "Uitmuntend", "en": "Excellent"}},
        ],
        "global_section_evaluation": True,
        "global_evaluation": True,
        "sections": [
            {
                "code": "onderzoeken",
                "title": {"nl": "Onderzoeken", "en": "Research"},
                "items": [
                    {"value": "stemvorkproeven", "label": {"nl": "Stemvorkproeven", "en": "Tuning fork tests"}},
                    {"value": "tonale_audiometrie", "label": {"nl": "Tonale audiometrie", "en": "Tonal audiometry"}},
                    {"value": "maskeren", "label": {"nl": "Maskeren", "en": "Masking"}},
                    {"value": "admittantiemetrie", "label": {"nl": "Admittantiemetrie", "en": "Admittance meter"}},
                    {"value": "spraakaudiometrie", "label": {"nl": "Spraakaudiometrie", "en": "Speech audiometry"}},
                    {"value": "kinderaudiometrie", "label": {"nl": "Kinderaudiometrie", "en": "Child audiometry"}},
                    {"value": "oto_akoestische_emissies", "label": {"nl": "Oto-akoestische emissies", "en": "Otoacoustic emissions"}},
                    {"value": "bera_assr_ecochg", "label": {"nl": "BERA/ASSR/EcochG", "en": "BERA/ASSR/EcochG"}},
                    {"value": "eng_vng", "label": {"nl": "ENG/VNG (calorische, rotatie, VEMP)", "en": "ENG/VNG (caloric, rotation, VEMP)"}},
                    {"value": "vng", "label": {"nl": "VNG (bedside testing + maneuvers)", "en": "VNG (bedside testing + maneuvers)"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "dossierstudies",
                "title": {"nl": "Dossierstudies", "en": "Case studies"},
                "items": [
                    {"value": "inhoudelijk", "label": {"nl": "Inhoudelijk", "en": "Content"}},
                    {"value": "structuur", "label": {"nl": "Structuur", "en": "Structure"}},
                    {"value": "integratie", "label": {"nl": "Integratie wetenschappelijke component", "en": "Integration scientific component"}},
                    {"value": "tijdstip_indienen", "label": {"nl": "Tijdstip indienen", "en": "Time of submission"}},
                    {"value": "adviezen", "label": {"nl": "Adviezen en tips", "en": "Advice and tips"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "verslaggeving",
                "title": {"nl": "Verslaggeving", "en": "Reporting"},
                "items": [
                    {"value": "doelstelling", "label": {"nl": "Inzicht in de doelstelling", "en": "Insight into the objective"}},
                    {"value": "methode", "label": {"nl": "Inzicht in de methode", "en": "Insight into the method"}},
                    {"value": "verloop", "label": {"nl": "Inzicht in het verloop", "en": "Insight into the course"}},
                    {"value": "resultaat", "label": {"nl": "Inzicht in het resultaat", "en": "Insight into the result"}},
                    {"value": "conclusie", "label": {"nl": "Conclusie / adviezen / tips", "en": "Conclusion / advice / tips"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "algemene_vaardigheden",
                "title": {"nl": "Algemene vaardigheden", "en": "General skills"},
                "items": [
                    {"value": "medische_fiche", "label": {"nl": "Medische fiche interpreteren", "en": "Interpreting medical records"}},
                    {"value": "implementeren_theorie", "label": {"nl": "Implementeren theorie in praktijk", "en": "Implementing theory in practice"}},
                    {"value": "accuratesse", "label": {"nl": "Accuratesse / stiptheid", "en": "Accuracy / punctuality"}},
                    {"value": "eigen_handelen", "label": {"nl": "Evaluatie - eigen handelen", "en": "Evaluation - own actions"}},
                    {"value": "eigen_stem", "label": {"nl": "Eigen stem, spraak en taal", "en": "Own voice, speech and language"}},
                    {"value": "aangepast_taalgebruik", "label": {"nl": "Aangepast mondeling taalgebruik (op maat van gesprekspartner)", "en": "Adapted oral language use (tailored to interlocutor)"}},
                    {"value": "correctheid_schrijven", "label": {"nl": "Correctheid van het schrijven", "en": "Correctness of writing"}},
                ],
                "cross_items": [],
                "add_remarks": True,
            },
            {
                "code": "sociale_vaardigheden",
                "title": {"nl": "Attitudes en sociale vaardigheden", "en": "Attitudes and social skills"},
                "items": [
                    {"value": "communicatieve_ingesteldheid", "label": {"nl": "Algemeen communicatieve ingesteldheid", "en": "General communicative attitude"}},
                    {"value": "relatie_teamleden", "label": {"nl": "Relatie / omgang met teamleden", "en": "Relationship / interaction with team members"}},
                    {"value": "relatie_patienten", "label": {"nl": "Relatie / omgang met patiënten", "en": "Relationship / interaction with patients"}},
                    {"value": "plaats_kenen", "label": {"nl": "Kent zijn / haar plaats binnen de setting", "en": "Knows his / her place within the setting"}},
                    {"value": "enthousiasme", "label": {"nl": "Enthousiasme en interesse", "en": "Enthusiasm and interest"}},
                    {"value": "vraagt_feedback", "label": {"nl": "Vraagt om verduidelijking en feedback", "en": "Asks for clarification and feedback"}},
                    {"value": "volgt_adviezen", "label": {"nl": "Gaat aan de slag met tips en adviezen", "en": "Gets started with tips and advice"}},
                    {"value": "leergierigheid", "label": {"nl": "Leergierigheid", "en": "Eagerness to learn"}},
                    {"value": "kritische_ingesteldheid", "label": {"nl": "Kritische ingesteldheid, durft zichzelf in vraag stellen", "en": "Critical attitude, dares to question himself"}},
                    {"value": "zelfstandigheid", "label": {"nl": "Zelfstandigheid", "en": "Independence"}},
                    {"value": "teamgerichtheid", "label": {"nl": "Teamgerichtheid (samenwerken)", "en": "Team orientation (collaboration)"}},
                    {"value": "flexibiliteit", "label": {"nl": "Flexibiliteit", "en": "Flexibility"}},
                    {"value": "deontologie", "label": {"nl": "Deontologie", "en": "Deontology"}},
                ],
                "cross_items": [],
                "add_remarks": True,
            }
        ],
    }


def get_audio_internship_evaluation_form_protetisch() -> dict:
    return {
        "description": description,
        "intermediate_evaluations": 1,
        "grades":[
            {"value": None, "label": {"nl": "n.v.t.", "en": "N/A"}},
            {"value": 1, "label": {"nl": "Onvoldoende", "en": "Insufficient"}},
            {"value": 3, "label": {"nl": "Net voldoende", "en": "Just sufficient"}},
            {"value": 5, "label": {"nl": "Voldoende", "en": "Sufficient"}},
            {"value": 6, "label": {"nl": "Goed", "en": "Good"}},
            {"value": 8, "label": {"nl": "Zeer goed", "en": "Very good"}},
            {"value": 9, "label": {"nl": "Uitmuntend", "en": "Excellent"}},
        ],
        "global_section_evaluation": True,
        "global_evaluation": True,
        "sections": [
            {
                "code": "onderzoeken",
                "title": {"nl": "Onderzoeken", "en": "Research"},
                "items": [
                    {"value": "tonale_audiometrie", "label": {"nl": "Tonale audiometrie", "en": "Tonal audiometry"}},
                    {"value": "spraakaudiometrie", "label": {"nl": "Spraakaudiometrie", "en": "Speech audiometry"}},
                    {"value": "lokalisatietests", "label": {"nl": "Lokalisatietests", "en": "Localization tests"}},
                    {"value": "lekdichtheidtests", "label": {"nl": "Lekdichtheidtests", "en": "Leakage tests"}},
                    {"value": "insertiemetingen", "label": {"nl": "Insertiemetingen", "en": "Insertion measurements"}},
                    {"value": "vragenlijsten", "label": {"nl": "Vragenlijsten", "en": "Questionnaires"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "protetisch_handelen",
                "title": {"nl": "Protetisch handelen", "en": "Prosthetic action"},
                "items": [
                    {"value": "intake", "label": {"nl": "Intake", "en": "Intake"}},
                    {"value": "oorafdrukken", "label": {"nl": "Oorafdrukken", "en": "Ear impressions"}},
                    {"value": "selectie_hoortoestel", "label": {"nl": "Selectie hoortoestel en oorstuk", "en": "Selection of hearing aid and earmold"}},
                    {"value": "aanpassen_hoortoestel", "label": {"nl": "Aanpassen hoortoestel", "en": "Adjusting hearing aid"}},
                    {"value": "selectie_hoorhulpmiddel", "label": {"nl": "Selectie hoorhulpmiddel", "en": "Selection of hearing aid"}},
                    {"value": "aanpassen_hoorhulpmiddel", "label": {"nl": "Aanpassen hoorhulpmiddel", "en": "Adjusting hearing aid"}},
                    {"value": "selectie_lawaaibescherming", "label": {"nl": "Selectie lawaaibescherming", "en": "Selection of noise protection"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "dossierstudies",
                "title": {"nl": "Dossierstudies", "en": "Case studies"},
                "items": [
                    {"value": "inhoudelijk", "label": {"nl": "Inhoudelijk", "en": "Content"}},
                    {"value": "structuur", "label": {"nl": "Structuur", "en": "Structure"}},
                    {"value": "integratie", "label": {"nl": "Integratie wetenschappelijke component", "en": "Integration scientific component"}},
                    {"value": "tijdstip_indienen", "label": {"nl": "Tijdstip indienen", "en": "Time of submission"}},
                    {"value": "adviezen", "label": {"nl": "Adviezen en tips", "en": "Advice and tips"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "verslaggeving",
                "title": {"nl": "Verslaggeving", "en": "Reporting"},
                "items": [
                    {"value": "doelstelling", "label": {"nl": "Inzicht in de doelstelling", "en": "Insight into the objective"}},
                    {"value": "methode", "label": {"nl": "Inzicht in de methode", "en": "Insight into the method"}},
                    {"value": "verloop", "label": {"nl": "Inzicht in het verloop", "en": "Insight into the course"}},
                    {"value": "resultaat", "label": {"nl": "Inzicht in het resultaat", "en": "Insight into the result"}},
                    {"value": "conclusie", "label": {"nl": "Conclusie / adviezen / tips", "en": "Conclusion / advice / tips"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "algemene_vaardigheden",
                "title": {"nl": "Algemene vaardigheden", "en": "General skills"},
                "items": [
                    {"value": "medische_fiche", "label": {"nl": "Medische fiche interpreteren", "en": "Interpreting medical records"}},
                    {"value": "implementeren_theorie", "label": {"nl": "Implementeren theorie in praktijk", "en": "Implementing theory in practice"}},
                    {"value": "accuratesse", "label": {"nl": "Accuratesse / stiptheid", "en": "Accuracy / punctuality"}},
                    {"value": "eigen_handelen", "label": {"nl": "Evaluatie - eigen handelen", "en": "Evaluation - own actions"}},
                    {"value": "eigen_stem", "label": {"nl": "Eigen stem, spraak en taal", "en": "Own voice, speech and language"}},
                    {"value": "aangepast_taalgebruik", "label": {"nl": "Aangepast mondeling taalgebruik (op maat van gesprekspartner)", "en": "Adapted oral language use (tailored to interlocutor)"}},
                    {"value": "correctheid_schrijven", "label": {"nl": "Correctheid van het schrijven", "en": "Correctness of writing"}},
                ],
                "cross_items": [],
                "add_remarks": True,
            },
            {
                "code": "sociale_vaardigheden",
                "title": {"nl": "Attitudes en sociale vaardigheden", "en": "Attitudes and social skills"},
                "items": [
                    {"value": "communicatieve_ingesteldheid", "label": {"nl": "Algemeen communicatieve ingesteldheid", "en": "General communicative attitude"}},
                    {"value": "relatie_teamleden", "label": {"nl": "Relatie / omgang met teamleden", "en": "Relationship / interaction with team members"}},
                    {"value": "relatie_patienten", "label": {"nl": "Relatie / omgang met patiënten", "en": "Relationship / interaction with patients"}},
                    {"value": "plaats_kenen", "label": {"nl": "Kent zijn / haar plaats binnen de setting", "en": "Knows his / her place within the setting"}},
                    {"value": "enthousiasme", "label": {"nl": "Enthousiasme en interesse", "en": "Enthusiasm and interest"}},
                    {"value": "vraagt_feedback", "label": {"nl": "Vraagt om verduidelijking en feedback", "en": "Asks for clarification and feedback"}},
                    {"value": "volgt_adviezen", "label": {"nl": "Gaat aan de slag met tips en adviezen", "en": "Gets started with tips and advice"}},
                    {"value": "leergierigheid", "label": {"nl": "Leergierigheid", "en": "Eagerness to learn"}},
                    {"value": "kritische_ingesteldheid", "label": {"nl": "Kritische ingesteldheid, durft zichzelf in vraag stellen", "en": "Critical attitude, dares to question himself"}},
                    {"value": "zelfstandigheid", "label": {"nl": "Zelfstandigheid", "en": "Independence"}},
                    {"value": "teamgerichtheid", "label": {"nl": "Teamgerichtheid (samenwerken)", "en": "Team orientation (collaboration)"}},
                    {"value": "flexibiliteit", "label": {"nl": "Flexibiliteit", "en": "Flexibility"}},
                    {"value": "deontologie", "label": {"nl": "Deontologie", "en": "Deontology"}},
                ],
                "cross_items": [],
                "add_remarks": True,
            }
        ],
    }


def get_logo_internship_evaluation_form_ma1() -> dict:
    return {
        "description": description,
        "intermediate_evaluations": 2,
        "grades":[
            {"value": None, "label": {"nl": "n.v.t.", "en": "N/A"}},
            {"value": 1, "label": {"nl": "Onvoldoende", "en": "Insufficient"}},
            {"value": 3, "label": {"nl": "Net voldoende", "en": "Just sufficient"}},
            {"value": 5, "label": {"nl": "Voldoende", "en": "Sufficient"}},
            {"value": 6, "label": {"nl": "Goed", "en": "Good"}},
            {"value": 8, "label": {"nl": "Zeer goed", "en": "Very good"}},
            {"value": 9, "label": {"nl": "Uitmuntend", "en": "Excellent"}},
        ],
        "global_section_evaluation": True,
        "global_evaluation": True,
        "sections": [
            {
                "code": "algemeen_kenis",
                "title": {"nl": "Algemeen logopedische kennis", "en": "General logopedic knowledge"},
                "items": [
                    {"value": "inzicht", "label": {"nl": "Inzicht in de pathologie en ernst", "en": "Insight into the pathology and severity"}},
                    {"value": "vakterminologie", "label": {"nl": "Gebruik van vakterminologie", "en": "Use of technical terminology"}},
                    {"value": "implementeren_theorie", "label": {"nl": "Implementeren theorie in praktijk", "en": "Implementing theory in practice"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "dossierstudies",
                "title": {"nl": "Dossierstudies", "en": "Case studies"},
                "items": [
                    {"value": "inhoudelijk", "label": {"nl": "Inhoudelijk", "en": "Content"}},
                    {"value": "structuur", "label": {"nl": "Structuur", "en": "Structure"}},
                    {"value": "integratie", "label": {"nl": "Integratie wetenschappelijke component", "en": "Integration scientific component"}},
                    {"value": "tijdstip_indienen", "label": {"nl": "Tijdstip van indienen", "en": "Time of submission"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "behandelingsplannen",
                "title": {"nl": "Behandelingsplannen", "en": "Treatment plans"},
                "items": [
                    {"value": "inhoudelijk", "label": {"nl": "Inhoudelijk", "en": "Content"}},
                    {"value": "structuur", "label": {"nl": "Structuur", "en": "Structure"}},
                    {"value": "tijdstip_indienen", "label": {"nl": "Tijdstip van indienen", "en": "Time of submission"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "verslaggeving_observaties",
                "title": {"nl": "Verslaggeving bij observaties", "en": "Reporting on observations"},
                "items": [
                    {"value": "doelstelling", "label": {"nl": "Inzicht in de doelstelling", "en": "Insight into the objective"}},
                    {"value": "methodologie", "label": {"nl": "Inzicht in de methodologie", "en": "Insight into the methodology"}},
                    {"value": "foutenanalyse", "label": {"nl": "Inzicht in het foutenanalyse", "en": "Insight into the error analysis"}},
                    {"value": "conclusie", "label": {"nl": "Conclusie / adviezen / tips", "en": "Conclusion / advice / tips"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "therapievoorbereiding",
                "title": {"nl": "Therapievoorbereiding", "en": "Therapy preparation"},
                "items": [
                    {"value": "formulering_doelstelling", "label": {"nl": "Formulering doelstelling", "en": "Formulation of the objective"}},
                    {"value": "werkvorm", "label": {"nl": "Werkvorm en materiaal", "en": "Working method and material"}},
                    {"value": "aangepaste_moeilijksheidsgraad", "label": {"nl": "Aangepaste moeilijkheidsgraad", "en": "Adapted level of difficulty"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "therapeutisch_handelen",
                "title": {"nl": "Therapeutisch handelen", "en": "Therapeutic action"},
                "items": [
                    {"value": "aanbreng", "label": {"nl": "Aanbreng", "en": "Presentation"}},
                    {"value": "feedback_patient", "label": {"nl": "Feedback naar de patiënt", "en": "Feedback to the patient"}},
                    {"value": "therapie_op_maat", "label": {"nl": "Therapie inhoud op maat van de patiënt", "en": "Therapy content tailored to the patient"}},
                    {"value": "aansluiten_vorige_therapie", "label": {"nl": "Aansluiten bij vorige therapie", "en": "Connecting to previous therapy"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "verslaggeving_behandelingen",
                "title": {"nl": "Verslaggeving bij behandelingen", "en": "Reporting on treatments"},
                "items": [
                    {"value": "foutenanalyse", "label": {"nl": "Foutenanalyse", "en": "Error analysis"}},
                    {"value": "evaluatie_eigne_handelen", "label": {"nl": "Evaluatie van eigen handelen", "en": "Evaluation of own actions"}},
                    {"value": "conclusies", "label": {"nl": "Conclusies naar volgende therapie", "en": "Conclusions for next therapy"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "onderzoek",
                "title": {"nl": "Onderzoek", "en": "Research"},
                "items": [
                    {"value": "voorbereiding", "label": {"nl": "Voorbereiding", "en": "Preparation"}},
                    {"value": "afname", "label": {"nl": "Afname", "en": "Sampling"}},
                    {"value": "foutenanalyse", "label": {"nl": "Foutenanalyse", "en": "Error analysis"}},
                    {"value": "scoring", "label": {"nl": "Scoring", "en": "Scoring"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "taal_spraak",
                "title": {"nl": "Taal en spraak", "en": "Language and speech"},
                "items": [
                    {"value": "correct_taalgebruik", "label": {"nl": "Correct / rijk mondeling taalgebruik", "en": "Correct / rich oral language use"}},
                    {"value": "aangepast_taalgebruik", "label": {"nl": "Aangepast mondeling taalgebruik (op maat van gesprekspartner)", "en": "Adapted oral language use (tailored to interlocutor)"}},
                    {"value": "articulatie", "label": {"nl": "Correctheid articulatie", "en": "Correctness of articulation"}},
                    {"value": "intonatie", "label": {"nl": "Intonatie, spreektempo, stemvolume", "en": "Intonation, speaking rate, voice volume"}},
                    {"value": "schriftelijk_taalgebruik", "label": {"nl": "Rijk schriftelijk taalgebruik", "en": "Rich written language use"}},
                    {"value": "spelling", "label": {"nl": "Correctheid spelling", "en": "Correctness of spelling"}},
                ],
                "cross_items": [
                    {"value": "actief", "label": {"nl": "Actief", "en": "Active"}},
                    {"value": "passief", "label": {"nl": "Pasief", "en": "Passive"}},
                ],
                "add_remarks": True,
            },
            {
                "code": "sociale_vaardigheden",
                "title": {"nl": "Attitudes en sociale vaardigheden", "en": "Attitudes and social skills"},
                "items": [
                    {"value": "communicatieve_ingesteldheid", "label": {"nl": "Algemeen communicatieve ingesteldheid", "en": "General communicative attitude"}},
                    {"value": "relatie_teamleden", "label": {"nl": "Relatie / omgang met teamleden", "en": "Relationship / interaction with team members"}},
                    {"value": "relatie_patienten", "label": {"nl": "Relatie / omgang met patiënten", "en": "Relationship / interaction with patients"}},
                    {"value": "plaats_kenen", "label": {"nl": "Kent zijn / haar plaats binnen de setting", "en": "Knows his / her place within the setting"}},
                    {"value": "enthousiasme", "label": {"nl": "Enthousiasme en interesse", "en": "Enthusiasm and interest"}},
                    {"value": "vraagt_feedback", "label": {"nl": "Vraagt om verduidelijking en feedback", "en": "Asks for clarification and feedback"}},
                    {"value": "volgt_adviezen", "label": {"nl": "Gaat aan de slag met tips en adviezen", "en": "Gets started with tips and advice"}},
                    {"value": "leergierigheid", "label": {"nl": "Leergierigheid", "en": "Eagerness to learn"}},
                    {"value": "kritische_ingesteldheid", "label": {"nl": "Kritische ingesteldheid, durft zichzelf in vraag stellen", "en": "Critical attitude, dares to question himself"}},
                    {"value": "zelfstandigheid", "label": {"nl": "Zelfstandigheid", "en": "Independence"}},
                    {"value": "teamgerichtheid", "label": {"nl": "Teamgerichtheid (samenwerken)", "en": "Team orientation (collaboration)"}},
                    {"value": "flexibiliteit", "label": {"nl": "Flexibiliteit", "en": "Flexibility"}},
                    {"value": "deontologie", "label": {"nl": "Deontologie", "en": "Deontology"}},
                    {"value": "accuratesse", "label": {"nl": "Accuratesse / stiptheid", "en": "Accuracy / punctuality"}},
                ],
                "cross_items": [],
                "add_remarks": True,
            }
        ],
    }
