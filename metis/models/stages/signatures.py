from django.db import models


class Signature(models.Model):
    student = models.ForeignKey("metis.Student", related_name="signatures", on_delete=models.PROTECT)
    text_entry = models.ForeignKey("metis.TextEntry", related_name="signatures", on_delete=models.PROTECT)
    signed_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "metis_log_signature"
