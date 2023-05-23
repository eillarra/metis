interface TextEntryType {
  code: string;
  signature_required: boolean;
  name_nl: string;
  name_en: string;
  name?: string;
}

interface EducationConfig {
  allow_different_blocks_per_user_in_project: boolean;
  project_text_types: TextEntryType[];
  place_text_types: TextEntryType[];
}
