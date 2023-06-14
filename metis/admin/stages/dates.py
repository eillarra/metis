from django.contrib import admin

from metis.models.stages.dates import ImportantDate


class ImportantDatesInline(admin.TabularInline):
    model = ImportantDate
    extra = 0
    # form
    raw_id_fields = ("period",)
