interface Questioning extends ApiObject {
  self: ApiEndpoint;
  rel_responses: ApiEndpoint;
  type: string;
  start_at: string;
  end_at: string;
  is_active: boolean;
  period: number;
  form_definition: CustomFormDefinition | TopsFormDefinition;
  email_subject: string;
  email_body: string;
  email_add_office_in_bcc: boolean;
  updated_at: string;
  updated_by: UserTiny;
  target_object_ids?: number[];
  stats?: {
    response_rate: number;
  };
  // -----
  has_email?: boolean;
  Period?: Period;
}
