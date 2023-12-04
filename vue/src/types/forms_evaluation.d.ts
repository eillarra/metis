interface EvaluationPeriod {
  intermediate: number;
  name: string;
  is_final: boolean;
  start_at: Date;
  end_at: Date;
  start: string;
  end: string;
}

interface EvaluationScore {
  value: str | null;
  label: Translation;
  points: number | null;
  only_for_global_score: boolean;
}

interface EvaluationItem {
  value: string;
  label: Translation;
  score_help_texts: [string, Translation][];
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
  global_score: string | null | undefined;
  sections: {
    [key: string]: {
      score: string | null | undefined;
      scores: {
        [key: string]: [string | null, string | null];
      };
      remarks?: string;
    };
  };
  global_remarks?: string;
}
