interface EvaluationGrade {
  value: number | null;
  label: Translation;
}

interface EvaluationItem {
  value: string;
  label: Translation;
}

interface EvaluationSection {
  code: string;
  title: Translation | null;
  description: Translation | null;
  items: EvaluationItem[];
  add_remarks: boolean;
}

interface EvaluationFormDefinition {
  title: Translation | null;
  description: Translation | null;
  grades: EvaluationGrade[];
  sections: EvaluationSection[];
}

interface EvaluationForm extends ApiObjectUpdated {
  definition: EvaluationFormDefinition;
  period: number;
  // -----
  Period?: Period;
}
