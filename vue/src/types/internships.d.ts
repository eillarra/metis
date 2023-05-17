interface Internship extends ApiObject {
  self: ApiEndpoint;
  rel_remarks: ApiEndpoint;
  student: Student | number | null;
  period: Period | number;
  track: TrackTiny | null;
  discipline: Discipline | null;
  start_date: string;
  end_date: string;
  project_place: number;
  custom_start_date: string | null;
  custom_end_date: string | null;
  place?: Place;
}
