from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    position = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "sparta.User",
        related_name="%(class)s_created_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "sparta.User",
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

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
