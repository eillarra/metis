interface Student extends ApiObject {
  self: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  project: Project | number;
  user: User | number;
  block: Block | number;
  track: Track | number | null;
  remark_count: number;
}

interface StudentUser extends User {
  student_set: Student[];
}
