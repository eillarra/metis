type EmailAddress = string;

interface Email extends ApiObject {
  sent_at: string;
  subject: string;
  to: EmailAddress[];
  bcc: EmailAddress[];
  reply_to: EmailAddress[];
  tags: string[];
  tag_set?: Set<string>;
}

interface FullEmail extends Email {
  body: string;
  internship: Internship;
}
