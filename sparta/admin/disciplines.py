from django.contrib import admin

from sparta.models.disciplines import Discipline


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_filter = ("education",)
    search_fields = ("code", "name")
