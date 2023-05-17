interface ProgramBlockTiny extends ApiObject {
  name: string;
  position: number;
}

interface ProgramBlock extends ProgramBlockTiny {
  internships: ProgramInternship[];
}

interface ProgramInternship extends ApiObject {
  name: string;
  block: number | ProgramBlockTiny;
  position: number;
  start_week: number;
  duration: number | null;
  updated_at: string;
  updated_by: UserTiny;
}

interface Program extends ApiObject {
  education: number | Education;
  name: string;
  blocks: ProgramBlock[];
  tracks: Track[];
  valid_from: string;
  valid_until: string;
  updated_at: string;
  updated_by: UserTiny;
}

interface TrackTiny extends ApiObject {
  name: string;
  program: int | Program;
}

interface Track extends TrackTiny {
  program_internships: number[];
  updated_at: string;
  updated_by: UserTiny;
}
