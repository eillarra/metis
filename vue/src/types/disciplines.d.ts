interface DisciplineTiny {
  id: number;
  code: string;
  name: string;
}

interface Discipline extends DisciplineTiny {
  self: string;
}
