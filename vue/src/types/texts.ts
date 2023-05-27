interface TextEntry extends ApiObject {
  self: ApiEndpoint;
  code: string;
  version: number;
  title_en: string;
  title_nl: string;
  text_en: string;
  text_nl: string;
  updated_at: string;
  updated_by: UserTiny;
  type?: string;
  title?: string;
  text?: string;
}
