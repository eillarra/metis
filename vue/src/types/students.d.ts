interface StudentRecords {
  id: number;
  project: ProjectTiny;
  block: ProgramBlockTiny;
  track: number | null;
}

interface Student extends BasicUser {
  id: number;
  student_records: StudentRecords[];
}
