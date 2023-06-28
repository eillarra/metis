from django.contrib import admin

from metis.models.rel.forms import CustomForm


@admin.register(CustomForm)
class CustomFormAdmin(admin.ModelAdmin):
    list_display = ("code", "project")
    list_filter = (
        "code",
        ("project", admin.RelatedOnlyFieldListFilter),
    )
