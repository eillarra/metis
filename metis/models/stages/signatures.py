from django.db import models
from django.urls import reverse
from uuid import uuid4

from ..base import NonEditableMixin


class Signature(NonEditableMixin, models.Model):
    student = models.ForeignKey("metis.Student", related_name="signatures", on_delete=models.PROTECT)
    text_entry = models.ForeignKey("metis.TextEntry", related_name="signatures", on_delete=models.PROTECT)
    signed_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    class Meta:
        db_table = "metis_log_signature"

    def get_absolute_url(self):
        return reverse("signature_pdf", kwargs={"uuid": self.uuid})
