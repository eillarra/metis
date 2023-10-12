interface Internship extends ApiObject {
  self: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  rel_timesheets: ApiEndpoint;
  student: number | null;
  track: number | null;
  period: number | null;
  mentors: Mentor[];
  discipline: number | null;
  start_date: string;
  end_date: string;
  project_place: number;
  status: string;
  updated_at: string;
  updated_by: UserTiny | null;
  // -----
  Student?: Student;
  Track?: Track;
  Period?: Period;
  Discipline?: Discipline;
  ProjectPlace?: ProjectPlace;
  Place?: Place;
}

interface Mentor extends ApiObject {
  user: UserLastLogin;
}
