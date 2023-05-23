from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Link(models.Model):
    """
    Online accounts and other links.
    """

    WEBSITE = "website"
    LINKEDIN = "linkedin"
    OTHER = "other"
    TYPES = (
        (WEBSITE, "Website"),
        (LINKEDIN, "LinkedIn"),
        (OTHER, "Other"),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="links")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(max_length=16, choices=TYPES, default=WEBSITE)
    url = models.URLField()

    class Meta:
        db_table = "metis_rel_link"


class LinksMixin(models.Model):
    links_cache = None
    links = GenericRelation(Link)

    class Meta:
        abstract = True

    def get_link(self, link_type: str) -> str | None:
        if not self.links_cache:
            self.links_cache = self.links.all()  # noqa
        for link in self.links_cache:
            if link.type == link_type:
                return link.url
        return None

    @property
    def website(self) -> str | None:
        return self.get_link(Link.WEBSITE)
