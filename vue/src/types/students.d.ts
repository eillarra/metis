interface Student extends ApiObject {
  self: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  project: number;
  user: number;
  block: number;
  track: number | null;
  remark_count: number;
  // -----
  Project?: Project;
  User?: StudentUser;
  Block?: Block;
  Track?: Track;
}

interface StudentUser extends User {
  student_set: Student[];
}
