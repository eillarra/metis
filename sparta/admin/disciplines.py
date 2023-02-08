from django.contrib import admin

from sparta.models.disciplines import Discipline


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    search_fields = ("name",)
