interface ProjectStudent extends ApiObject {
  self: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  project: ProjectTiny;
  user: number;
  block: ProgramBlockTiny;
  track: number | null;
  remark_count: number;
}

interface Student extends User {
  student_set: ProjectStudent[];
}
