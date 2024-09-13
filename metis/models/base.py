from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from .rel.snapshots import Snapshot, save_snapshot
from .validators import validate_list_of_strings


class NonEditableMixin(models.Model):
    """Models with this mixin can only be created, never edited."""

    class Meta:  # noqa: D106
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """Raise an error if we try to edit an existing model.

        :raises ValueError: If the model is not new.
        """
        if self.pk:
            raise ValueError("This model is not editable.")
        super().save(*args, **kwargs)


class TagsMixin(models.Model):
    """A mixin to add tags to a model."""

    tags = models.JSONField(default=list, validators=[validate_list_of_strings])

    class Meta:  # noqa: D106
        abstract = True


class BaseModel(models.Model):
    """Base model for models that require auditing."""

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

    class Meta:  # noqa: D106
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """TODO: find the best way of always enforcing checks."""
        if not self.pk and not self.updated_by:
            self.updated_by = self.created_by
        # self.full_clean()
        super().save(*args, **kwargs)
        save_snapshot(self.__class__, self, user=self.updated_by)
