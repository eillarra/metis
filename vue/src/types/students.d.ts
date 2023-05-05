interface StudentObjects {
  id: number;
  project: ProjectTiny;
  block: ProgramBlockTiny;
  track: number | null;
}

interface Student extends UserTiny {
  id: number;
  student_set: StudentObjects[];
}
