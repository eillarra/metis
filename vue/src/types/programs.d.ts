interface ProgramBlockTiny {
  id: number;
  name: string;
  position: number;
}

interface ProgramInternship {
  id: number;
  name: string;
  block: ProgramBlockTiny;
  start_week: number;
  duration: number | null;
}

interface Program {
  id: number;
  name: string;
  blocks: ProgramBlockTiny[];
  valid_from: string;
  valid_until: string;
  updated_at: string;
  updated_by: BasicUser;
}

interface TrackTiny {
  id: number;
  name: string;
  program: int | Program;
}
