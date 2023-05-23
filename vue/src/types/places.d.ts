interface Region extends ApiObject {
  name: string;
  country: string;
}

interface Place extends ApiObject {
  self: ApiEndpoint;
  rel_contacts: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  rel_texts: ApiEndpoint;
  parent: null | ApiEndpoint;
  education: number;
  type: string;
  name: string;
  code: string;
  region: Region | null;
  contacts: Contact[];
  updated_at: string;
  updated_by: UserTiny | null;
  remark_count: number;
}

interface ProjectPlace extends ApiObject {
  self: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  project: number;
  place: Place;
  disciplines: Discipline[];
  updated_at: string;
  updated_by: UserTiny | null;
  remark_count: number;
}

interface Contact extends ApiObject {
  self: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  user: UserTiny;
  is_staff: boolean;
  is_mentor: boolean;
  remark_count: number;
  place: Place | number;
  updated_at: string;
  updated_by: UserTiny | null;
}
