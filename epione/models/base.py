from django.db import models

from .rel.snapshots import SnapshotsMixin


class BaseModel(SnapshotsMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "epione.User",
        related_name="%(class)s_created_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "epione.User",
        related_name="%(class)s_updated_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """TODO: find the best way of always enforcing checks."""
        # self.full_clean()
        super().save(*args, **kwargs)
