from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .form_builder.custom_forms import CustomForm


class Translation(BaseModel):
    """A translation for a field label or description."""

    nl: str
    en: str


class TextEntryType(BaseModel):
    """A type of text entry for a project or place."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    code: str
    title: Translation


class ProjectTextEntryType(TextEntryType):
    """A text entry type for a project."""

    signature_required: bool = True


class PlaceTextEntryType(TextEntryType):
    """A text entry type for a place."""

    editable_by_place: bool = True


class EducationConfig(BaseModel):
    """General configuration for an education."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    allow_different_blocks_per_user_in_project: bool = Field(
        default=True,
        description="Whether a user can be in different Blocks for the same Project",
    )
    automatic_internship_approval: bool = Field(
        default=True,
        description="Whether internships are automatically approved when they are created",
    )
    email_remind_before: list[int] = Field(
        default=[0, 3, 7],
        description="The number of days before a deadline to send email reminders",
    )
    project_text_types: list[ProjectTextEntryType]
    place_text_types: list[PlaceTextEntryType] = []
    place_set_disciplines_per_block: bool = Field(
        default=False,
        description="Whether the disciplines for a place are set per Block (e.g. Ba3, Ma1, Ma2), or for the Project",
    )
    place_contact_is_staff: bool = Field(
        default=False,
        description="Whether staff level contacts are allowed, or just a simple contact > mentor > admin hierarchy",
    )
    place_contact_welcome_email: bool = Field(
        default=True,
        description="Whether a welcome email is sent to new contacts created by the education office",
    )
    student_update_dates: bool = Field(
        default=False,
        description="Whether students can update their internship dates",
    )
    timesheets_extra_form: CustomForm | None = Field(
        default=None,
        description="A custom form to add extra fields to timesheets",
    )

    @field_validator("project_text_types")
    def validate_project_text_types(cls, v):
        """Validate project_text_types checking for required entry codes."""
        required = {"project.internship_agreement", "project.privacy_agreement"}
        codes = {c.code for c in v}
        for code in required:
            if code not in codes:
                raise ValueError(f"`project_text_types` must contain and entry with code `{code}`")
        return v


def validate_education_configuration(config):
    """Validate an education configuration."""
    try:
        EducationConfig(**config)
    except (TypeError, ValidationError) as exc:
        raise ValueError(exc) from exc
