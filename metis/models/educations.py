from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from modeltranslation.translator import TranslationOptions

from metis.services.configurator import EducationConfig, validate_education_configuration
from .base import BaseModel


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
    office_email = models.EmailField(blank=True, null=True)
    config = models.JSONField(default=dict)

    def clean(self) -> None:
        if self.config:
            try:
                validate_education_configuration(self.config)
            except ValueError as e:
                raise ValidationError({"config": str(e)})
        return super().clean()

    def __str__(self) -> str:
        return self.short_name

    def can_be_managed_by(self, user) -> bool:
        return self.office_members.filter(pk=user.pk).exists()

    def get_office_url(self) -> str:
        return reverse("education_office", args=[self.code])

    def get_student_area_url(self) -> str:
        return reverse("student_area", args=[self.code])

    @property
    def configuration(self) -> dict | None:
        return EducationConfig(**self.config).dict() if self.config else None


class EducationTranslationOptions(TranslationOptions):
    fields = ("name", "short_name", "description")
