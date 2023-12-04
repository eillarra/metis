from uuid import uuid4

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from ..base import NonEditableMixin


class Signature(NonEditableMixin, models.Model):
    """A signature."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="signatures")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey("metis.User", related_name="signatures", on_delete=models.PROTECT)
    signed_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    class Meta:  # noqa: D106
        db_table = "metis_log_signature"

    def __str__(self) -> str:
        return str(self.uuid)

    def get_absolute_url(self):
        """Get the URL of the PDF version of the signature."""
        return reverse("signature_pdf", kwargs={"uuid": self.uuid})


class SignaturesMixin(models.Model):
    """Mixin for models that can be signed."""

    signatures = GenericRelation(Signature)

    class Meta:  # noqa: D106
        abstract = True
