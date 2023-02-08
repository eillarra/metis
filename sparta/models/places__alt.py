from django.db import models

from ..base import BaseModel


class Service(BaseModel):
    name = models.CharField(max_length=160)


class Region(BaseModel):
    is_active = models.BooleanField(default=True)
    is_visible_to_students = models.BooleanField(default=True)
    name = models.CharField(max_length=160)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TrainingPlace(BaseModel):
    GENERAL = "general"
    PRIVATE = "private"
    HOSPITAL = "hospital"

    name = models.CharField(max_length=160)
    type = models.CharField(max_length=16, default=HOSPITAL, editable=False)
    region = models.ForeignKey("sparta.Region", on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField("sparta.Service", related_name="places")

    accesibility = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "sparta_training_place"

    def __str__(self) -> str:
        return self.name


class Ward(models.Model):
    place = models.ForeignKey("sparta.TrainingPlace", related_name="wards", on_delete=models.CASCADE)

    class Meta:
        db_table = "sparta_training_place_ward"


class Contact(models.Model):
    place = models.ForeignKey("sparta.TrainingPlace", related_name="contacts", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    phone = models.CharField(max_length=160)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = "sparta_training_place_contact"

    def __str__(self) -> str:
        return self.name
