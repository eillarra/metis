interface EvaluationScore {
  value: str | null;
  label: Translation;
  points: number | null;
  only_for_global_score: boolean;
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
  cross_items: EvaluationItem[];
  with_remarks: boolean;
}

interface EvaluationFormDefinition {
  title: Translation | null;
  description: Translation | null;
  intermediate_evaluations: number;
  scores: EvaluationScore[];
  sections: EvaluationSection[];
  with_global_remarks: boolean;
}

interface EvaluationForm extends ApiObjectUpdated {
  definition: EvaluationFormDefinition;
  period: number;
  // -----
  Period?: Period;
}

interface EvaluationData {
  global_score: string | null;
  sections: {
    [key: string]: {
      score: string | null;
      scores: {
        [key: string]: [string | null, string | null];
      };
      remarks?: string;
    };
  };
  global_remarks?: string;
}
