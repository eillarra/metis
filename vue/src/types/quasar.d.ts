interface QuasarAutocompleteOption {
  id: number;
  name: string;
  caption: string;
  disable?: boolean;
}

interface QuasarSelectOption {
  label: string;
  value: string;
}

interface QuasarDateRange {
  from: string;
  to: string;
}
