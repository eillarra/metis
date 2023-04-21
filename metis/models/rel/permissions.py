from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Permission(models.Model):
    """
    ACL permissions.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="perms")
    object_id = models.IntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey("metis.User", blank=True, related_name="perms", on_delete=models.CASCADE)

    class Meta:
        db_table = "metis_rel_permission"
        unique_together = ["content_type", "object_id", "user"]

    def __str__(self) -> str:
        return self.user


class PermissionsMixin(models.Model):
    acl = GenericRelation(Permission)

    class Meta:
        abstract = True
