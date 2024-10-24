interface Internship extends ApiObject {
  self: ApiEndpoint;
  rel_absences: ApiEndpoint;
  rel_evaluations: ApiEndpoint;
  rel_files: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  rel_timesheets: ApiEndpoint;
  uuid: string;
  student: number | null;
  track: number | null;
  period: number | null;
  mentors: Mentor[];
  discipline: number | null;
  start_date: string;
  end_date: string;
  project_place: number;
  status: string;
  is_approved: boolean;
  updated_at: string;
  updated_by: UserTiny | null;
  tags: Tags;
  // -----
  evaluation_periods?: [number, string, string, string][];
  // -----
  Student?: Student;
  Track?: Track;
  Period?: Period;
  Discipline?: Discipline;
  ProjectPlace?: ProjectPlace;
  Place?: Place;
  EvaluationForm?: EvaluationForm;
  // -----
  _tags_dict?: TagsDict;
}

interface Mentor extends ApiObject {
  user: UserLastLogin;
}

interface Evaluation extends ApiObject {
  uuid: string;
  intermediate: number;
  name: string;
  url: string;
  form: number;
  data: EvaluationData;
  is_approved: boolean;
  is_self_evaluation: boolean;
  // -----
  form_definition?: EvaluationFormDefinition;
  Form?: EvaluationForm;
  evaluation_periods?: [number, string, string][];
}
