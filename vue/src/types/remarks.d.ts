interface Remark extends ApiObject {
  self: ApiEndpoint;
  text: string;
  updated_at: string;
  updated_by: UserTiny;
  type?: string;
  // -----
  is_mine?: boolean;
  stamp?: string;
}
