interface Contact {
  id: number;
  user: TinyUser;
  is_staff: boolean;
  is_mentor: boolean;
  institutions?: Institution[];
}

interface Place {
  id: number;
  institution: Institution;
  disciplines: Discipline[];
  contacts: Contact[];
}
