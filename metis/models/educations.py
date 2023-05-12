from django.db import models
from django.urls import reverse
from modeltranslation.translator import TranslationOptions
from typing import TYPE_CHECKING

from .base import BaseModel

if TYPE_CHECKING:
    from .users import User


class Faculty(BaseModel):
    name = models.CharField(max_length=160)

    class Meta:
        verbose_name_plural = "faculties"

    def __str__(self) -> str:
        return self.name


class FacultyTranslationOptions(TranslationOptions):
    fields = ("name",)


class Education(BaseModel):
    faculty = models.ForeignKey(Faculty, related_name="educations", on_delete=models.PROTECT)
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=160)
    short_name = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    office_members = models.ManyToManyField("metis.User", related_name="education_set", blank=True)

    def __str__(self) -> str:
        return self.short_name

    def can_be_managed_by(self, user) -> bool:
        return user.is_staff or self.office_members.filter(pk=user.pk).exists()

    def get_office_url(self) -> str:
        return reverse("office:app", args=[self.code])


class EducationTranslationOptions(TranslationOptions):
    fields = ("name", "short_name", "description")
