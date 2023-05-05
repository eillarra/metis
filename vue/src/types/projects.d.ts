interface ProjectTiny {
  id: number;
  name: string;
}

interface Project extends ProjectTiny {
  id: number;
  self: ApiEndpoint;
  rel_internships: ApiEndpoint;
  rel_places: ApiEndpoint;
  rel_students: ApiEndpoint;
  updated_at: string;
  updated_by: UserTiny;
}
