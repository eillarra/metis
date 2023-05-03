interface Internship {
  id: number;
  place: int | Place;
  student: int | Student | null;
  program_internship: ProgramInternship;
  track: TrackTiny | null;
  discipline: Discipline | null;
}
