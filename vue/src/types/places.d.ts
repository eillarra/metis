interface Address extends ApiObject {
  self: ApiEndpoint;
  address: string;
  postcode: string;
  city: string;
  country: string;
  mapbox_feature: object;
}

interface PlaceType extends ApiObject {
  name: string;
}

interface Place extends ApiObject {
  self: ApiEndpoint;
  rel_addresses: ApiEndpoint;
  rel_contacts: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  rel_texts: ApiEndpoint;
  parent: null | ApiEndpoint;
  education: number;
  type: number;
  name: string;
  code: string;
  contacts: Contact[];
  updated_at: string;
  updated_by: UserTiny | null;
  remark_count: number;
  // -----
  Type?: PlaceType;
}

interface ProjectPlaceTiny extends ApiObject {
  self: ApiEndpoint;
  rel_form_responses: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  project: number;
  place: number;
  disciplines: number[];
  availability_set: ProjectPlaceAvailability[];
  updated_at: string;
  updated_by: UserTiny | null;
  remark_count: number;
  // -----
  Disciplines?: Discipline[];
  Place?: Place;
  Project?: Project;
  // -----
  _periods: Set<number>;
}

interface ProjectPlace extends ProjectPlaceTiny {
  place: Place;
}

interface ProjectPlaceAvailability extends ApiObject {
  period: number;
  min: number;
  max: number;
  // -----
  Period?: Period;
}

interface ProjectPlaceOption {
  value: number;
  label: string;
  place_id: number;
  disciplines: string;
}

interface Contact extends ApiObject {
  self: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  user: UserLastLogin;
  is_admin: boolean;
  is_staff: boolean;
  is_mentor: boolean;
  remark_count: number;
  place: number;
  updated_at: string;
  updated_by: UserTiny | null;
  // -----
  Place?: Place;
}

interface ContactPlace {
  id: number;
  name: string;
}
