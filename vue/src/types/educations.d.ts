interface Education {
  id: number;
  self: ApiEndpoint;
  rel_places: ApiEndpoint;
  rel_programs: ApiEndpoint;
  rel_projects: ApiEndpoint;
  url: Url;
  code: string;
  name: string;
  short_name: string;
  description: string | null;
  disciplines: Discipline[];
  office_members: UserTiny[];
}
