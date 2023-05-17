interface Faculty extends ApiObject {
  name: string;
}

interface Education extends ApiObject {
  self: ApiEndpoint;
  rel_places: ApiEndpoint;
  rel_programs: ApiEndpoint;
  rel_projects: ApiEndpoint;
  url: Url;
  faculty: Faculty;
  code: string;
  name: string;
  short_name: string;
  description: string | null;
  disciplines: Discipline[];
  office_members: UserTiny[];
}
