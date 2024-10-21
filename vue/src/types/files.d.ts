interface RelatedFile extends ApiObject {
  url: Url;
  code: string;
  version: number;
  description: string;
  created_at: string;
  updated_at: string;
  tags: Tags;
  // -----
  _tags_dict?: TagsDict;
}
