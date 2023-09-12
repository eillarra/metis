interface ProjectTiny extends ApiObject {
  name: string;
  full_name: string;
}

interface Project extends ProjectTiny {
  self: ApiEndpoint;
  rel_internships: ApiEndpoint;
  rel_places: ApiEndpoint;
  rel_students: ApiEndpoint;
  rel_texts: ApiEndpoint;
  education: number;
  periods: Period[];
  questionings: Questioning[];
  start_date: string;
  end_date: string;
  updated_at: string;
  updated_by: UserTiny;
  // -----
  Education?: Education;
}

interface Period extends ApiObject {
  program_internship: number;
  name: string;
  start_date: string;
  end_date: string;
  updated_at: string;
  updated_by: UserTiny;
  // -----
  ProgramInternship?: ProgramInternship;
}

interface Questioning extends ApiObject {
  type: string;
  start_at: string;
  end_at: string;
  is_active: boolean;
  period: number;
  form_definition: CustomFormDefinition;
  updated_at: string;
  updated_by: UserTiny;
  // -----
  Period?: Period;
}
