interface ProgramBlockTiny {
  id: number;
  name: string;
  position: number;
}

interface ProgramBlock extends ProgramBlockTiny {
  internships: ProgramInternship[];
}

interface ProgramInternship {
  id: number;
  name: string;
  block: number | ProgramBlockTiny;
  start_week: number;
  duration: number | null;
  updated_at: string;
  updated_by: UserTiny;
}

interface Program {
  id: number;
  name: string;
  blocks: ProgramBlock[];
  tracks: Track[];
  valid_from: string;
  valid_until: string;
  updated_at: string;
  updated_by: UserTiny;
}

interface TrackTiny {
  id: number;
  name: string;
  program: int | Program;
}

interface Track extends TrackTiny {
  program_internships: number[];
  updated_at: string;
  updated_by: UserTiny;
}
