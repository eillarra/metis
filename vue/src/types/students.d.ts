interface StudentObjects {
  id: number;
  project: ProjectTiny;
  block: ProgramBlockTiny;
  track: number | null;
}

interface Student extends BasicUser {
  id: number;
  student_objects: StudentObjects[];
}
