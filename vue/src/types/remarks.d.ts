interface Remark extends ApiObject {
  self: ApiEndpoint;
  text: string;
  updated_at: string;
  updated_by: UserTiny;
  tags: Tags;
  // -----
  _tags_dict?: TagsDict;
  type?: string;
  is_mine?: boolean;
  stamp?: string;
}
