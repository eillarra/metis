interface Student extends ApiObject {
  self: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  project: ProjectTiny;
  user: number;
  block: ProgramBlockTiny;
  track: number | null;
  remark_count: number;
}

interface StudentUser extends User {
  student_set: Student[];
}
