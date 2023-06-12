from django.db import models

from .base import BaseModel


class EmailTemplate(BaseModel):
    """
    Email templates are used to send emails to students, contacts, mentors, etc.
    Templates can be different by education; if no education is specified, the template is shared by all educations.
    """

    NO_REPLY = "noreply@ugent.be"

    education = models.ForeignKey(
        "metis.Education", related_name="email_templates", on_delete=models.PROTECT, null=True, blank=True
    )
    code = models.CharField(max_length=64)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    obj_class = models.CharField(max_length=64, null=True, blank=True)
    add_office_in_bcc = models.BooleanField(default=False)

    class Meta:
        db_table = "metis_email_template"
        ordering = ["education", "code"]
        unique_together = ("education", "code")

    def __str__(self) -> str:
        return f"{self.education} - {self.code}"

    def can_be_managed_by(self, user) -> bool:
        return self.education.can_be_managed_by(user) if self.education else False

    @property
    def bcc(self) -> list[str]:
        return (
            [self.education.office_email]
            if self.add_office_in_bcc and self.education and self.education.office_email
            else []
        )

    @property
    def reply_to(self) -> list[str]:
        return [self.education.office_email] if self.education and self.education.office_email else [self.NO_REPLY]


class EmailLog(models.Model):
    """
    Log of sent emails.
    """

    template = models.ForeignKey(EmailTemplate, related_name="logs", on_delete=models.PROTECT)
    user = models.ForeignKey("metis.User", related_name="email_logs", on_delete=models.PROTECT, null=True, blank=True)
    to = models.CharField(max_length=255)
    bcc = models.CharField(max_length=255, null=True, blank=True)
    reply_to = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "metis_log_email"

    def __str__(self) -> str:
        return f"{self.template} - {self.user} - {self.sent_at}"
