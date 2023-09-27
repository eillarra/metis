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
  fieldsets: Fieldset[];
  title?: Translation;
  description?: Translation;
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
  description?: Translation;
  type: 'project_places' | 'regions';
  num_tops: number;
}

interface TopsForm extends ApiObjectUpdated {
  code: 'student_tops';
  definition: TopsFormDefinition;
}
