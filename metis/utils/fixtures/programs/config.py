def get_basic_education_config() -> dict:
    """Return a basic Education configuration."""
    return {
        "allow_different_blocks_per_user_in_project": False,
        "automatic_internship_approval": False,
        "project_text_types": [
            {
                "code": "project.internship_agreement",
                "title": {"en": "Internship agreement", "nl": "Stage raamovereenkomst"},
                "signature_required": True,
            },
            {
                "code": "project.privacy_agreement",
                "title": {"en": "Privacy agreement", "nl": "Privacy verklaring"},
                "signature_required": True,
            },
        ],
    }
