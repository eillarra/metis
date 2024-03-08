interface Faculty extends ApiObject {
  name: string;
}

interface EducationTiny extends ApiObject {
  code: string;
  short_name: string;
  office_email?: string;
  configuration: EducationConfig | null;
}

interface Education extends EducationTiny {
  self: ApiEndpoint;
  rel_places: ApiEndpoint;
  rel_programs: ApiEndpoint;
  rel_projects: ApiEndpoint;
  url: Url;
  faculty: Faculty;
  name: string;
  description: string | null;
  disciplines: Discipline[];
  office_members: UserTiny[];
  office_email: string | null;
  place_types: PlaceType[];
}
