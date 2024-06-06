interface QuasarAutocompleteOption {
  id: number;
  name: string;
  caption: string;
  disable?: boolean;
}

interface QuasarDateRange {
  from: string;
  to: string;
}

interface QuasarSelectOption {
  label: string;
  value: string;
}

interface QuasarTableColumn {
  name: string;
  label: string;
  field: string | ((row: unknown) => unknown);
  required?: boolean | undefined;
  align?: 'left' | 'right' | 'center' | undefined;
  sortable?: boolean | undefined;
  sort?: ((a: unknown, b: unknown, rowA: unknown, rowB: unknown) => number) | undefined;
  headerStyle?: string | undefined;
  headerClasses?: string | undefined;
}

interface QuasarTableRow {
  _self: unknown;
  _hide_selection?: boolean | undefined;
  [key: string]: unknown;
}
