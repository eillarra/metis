interface Translation {
  nl: string;
  en: string;
}

interface TextEntryType {
  code: string;
  title: Translation;
}

interface ProjectTextEntryType extends TextEntryType {
  signature_required: boolean;
}

interface PlaceTextEntryType extends TextEntryType {
  editable_by_place: boolean;
}

interface EducationConfig {
  allow_different_blocks_per_user_in_project: boolean;
  automatic_internship_approval: boolean;
  project_text_types: ProjectTextEntryType[];
  place_text_types: PlaceTextEntryType[];
  place_set_disciplines_per_block: boolean;
  place_contact_is_staff: boolean;
  place_contact_welcome_email: boolean;
  student_update_dates: boolean;
  timesheets_extra_form: CustomFormDefinition | null;
}
