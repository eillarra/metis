from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from uuid import uuid4

from ..base import NonEditableMixin


class Signature(NonEditableMixin, models.Model):
    """
    A signature.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="signatures")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey("metis.User", related_name="signatures", on_delete=models.PROTECT)
    signed_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    class Meta:
        db_table = "metis_log_signature"

    def get_absolute_url(self):
        return reverse("signature_pdf", kwargs={"uuid": self.uuid})


class SignaturesMixin(models.Model):
    remarks = GenericRelation(Signature)

    class Meta:
        abstract = True
