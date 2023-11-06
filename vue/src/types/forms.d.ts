interface Translation {
  nl: string;
  en: string;
}

interface TranslatedFieldOption {
  value: string | number;
  label: string;
}

interface FieldOption {
  value: string | number;
  label: Translation;
}

interface FormField {
  type: string;
  code: string;
  label: Translation;
  required?: boolean; // TODO: remove ?
  collapsed?: boolean; // TODO: remove ?
}

interface InputField extends FormField {
  type: 'text' | 'textarea' | 'number' | 'date' | 'email' | 'tel' | 'url';
  mask?: string;
  placeholder?: Translation;
}

interface ChoiceField extends FormField {
  type: 'select' | 'option_group';
  options: (FieldOption | TranslatedFieldOption)[];
  multiple?: boolean; // TODO: remove ?
  other_option?: 'other';
}

interface GridField extends FormField {
  type: 'option_grid';
  options: (FieldOption | TranslatedFieldOption)[];
  columns: (FieldOption | TranslatedFieldOption)[];
}

interface Fieldset {
  fields: (InputField | ChoiceField | TimetableField)[];
  legend?: Translation;
  description?: Translation;
}

interface CustomFormDefinition {
  title?: Translation;
  task_cta?: Translation;
  description?: Translation;
  fieldsets: Fieldset[];
}

type CustomFormData = Record<string, string | number | string[] | number[]>;

interface CustomFormResponse extends ApiObjectUpdated {
  self: ApiEndpoint;
  questioning: number;
  object_id: number;
  data: CustomFormData;
  // -----
  _object?: Student | ProjectPlace;
}

interface TopsFormDefinition {
  title?: Translation;
  task_cta?: Translation;
  description?: Translation;
  type: 'project_places' | 'regions';
  num_tops: number;
  require_motivation: boolean;
  triage_question?: Translation;
}

interface TopsForm extends ApiObjectUpdated {
  code: 'student_tops';
  definition: TopsFormDefinition;
}

interface TopsFormData {
  tops: number[] | null;
  motivation?: Record<number, string>;
}

interface TopsFormResponse extends CustomFormResponse {
  data: TopsFormData;
}
