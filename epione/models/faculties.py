from django.db import models
from modeltranslation.translator import TranslationOptions

from .base import BaseModel
from .users import User
from .rel.permissions import PermissionsMixin


class Faculty(BaseModel):
    name = models.CharField(max_length=160)
    full_name = models.CharField(max_length=160)

    class Meta:
        verbose_name_plural = "faculties"

    def __str__(self) -> str:
        return self.name


class FacultyTranslationOptions(TranslationOptions):
    fields = ("name", "full_name")


class Education(PermissionsMixin, BaseModel):
    faculty = models.ForeignKey(Faculty, related_name="educations", on_delete=models.PROTECT)
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=160)
    short_name = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    office_members = models.ManyToManyField("epione.User", related_name="educations", blank=True)

    def __str__(self) -> str:
        return self.short_name

    def can_be_managed_by(self, user: "User") -> bool:
        return user.is_staff or self.office_members.filter(id=user.id).exists()


class EducationTranslationOptions(TranslationOptions):
    fields = ("name", "short_name", "description")