from typing import TYPE_CHECKING, Optional

from django.db import models

from .base import BaseModel


if TYPE_CHECKING:
    from .stages.internships import Internship


class EmailTemplate(BaseModel):
    """Email template model.

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
    add_office_in_bcc = models.BooleanField(default=False)
    language = models.CharField(max_length=2, default="nl")

    class Meta:  # noqa: D106
        db_table = "metis_email_template"
        ordering = ["education", "code"]
        unique_together = ("education", "code")

    def __str__(self) -> str:
        return f"{self.education} - {self.code}"

    def can_be_managed_by(self, user) -> bool:
        return self.education.can_be_managed_by(user) if self.education else False

    @property
    def bcc(self) -> list[str]:
        """Get bcc email address."""
        return (
            [self.education.office_email]
            if self.add_office_in_bcc and self.education and self.education.office_email
            else []
        )

    @property
    def reply_to(self) -> list[str]:
        """Get reply-to email address."""
        return [self.education.office_email] if self.education and self.education.office_email else [self.NO_REPLY]


class EmailLog(models.Model):
    """Log of sent emails."""

    project = models.ForeignKey(
        "metis.Project", related_name="email_logs", on_delete=models.SET_NULL, null=True, blank=True
    )
    template = models.ForeignKey(EmailTemplate, related_name="logs", on_delete=models.SET_NULL, null=True, blank=True)
    from_email = models.CharField(max_length=255)
    to = models.JSONField(default=list)
    bcc = models.JSONField(default=list)
    reply_to = models.JSONField(default=list)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    tags = models.JSONField(default=list)

    class Meta:  # noqa: D106
        db_table = "metis_log_email"

    def __str__(self) -> str:
        return f"{self.from_email} to {','.join(self.to)} - ({self.sent_at})"

    @property
    def internship(self) -> Optional["Internship"]:
        """Get internship related to the email. Only if tags contain 'internship.id:{id}'."""
        if self.project and any(tag.startswith("internship.id:") for tag in self.tags):
            internship_id = next((tag.split(":")[1] for tag in self.tags if tag.startswith("internship.id:")), None)
            if internship_id:
                try:
                    return self.project.internships.get(id=internship_id)
                except self.project.internships.model.DoesNotExist:
                    return None
        return None
