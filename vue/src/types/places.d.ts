interface Region {
  id: number;
  name: string;
  country: string;
}

interface Place {
  id: number;
  self: ApiEndpoint;
  name: string;
  type: string;
  region: Region | null;
}

interface EducationPlace {
  id: number;
  education: number | Education;
  place: Place;
  code: string;
  contacts: Contact[];
}

interface ProjectPlace {
  id: number;
  project: number | Project;
  place: Place;
  disciplines: Discipline[];
}

interface Contact {
  id: number;
  user: UserTiny;
  is_staff: boolean;
  is_mentor: boolean;
  places?: Place[];
}
