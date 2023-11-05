from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from .rel.snapshots import Snapshot, save_snapshot


class NonEditableMixin(models.Model):
    """Models with this mixin can only be created, never edited."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if self.pk:
            raise ValueError("This model is not editable.")
        super().save(*args, **kwargs)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "metis.User",
        related_name="%(class)s_created_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "metis.User",
        related_name="%(class)s_updated_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )
    snapshots = GenericRelation(Snapshot)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """TODO: find the best way of always enforcing checks."""
        if not self.pk and not self.updated_by:
            self.updated_by = self.created_by
        # self.full_clean()
        super().save(*args, **kwargs)
        save_snapshot(self.__class__, self, user=self.updated_by)
