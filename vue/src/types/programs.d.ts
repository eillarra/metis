interface ProgramBlockTiny {
  id: number;
  name: string;
  position: number;
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
