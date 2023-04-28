interface Region {
  id: number;
  name: string;
  country: string;
}

interface Place {
  id: number;
  name: string;
  type: string;
  region: Region | null;
  disciplines: DisciplineTiny[];
}
