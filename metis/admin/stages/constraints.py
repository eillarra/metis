from django.contrib.contenttypes.admin import GenericTabularInline

from metis.models.disciplines import Discipline
from metis.models.stages.constraints import DisciplineConstraint


class DisciplineConstraintsInline(GenericTabularInline):
    model = DisciplineConstraint
    classes = ("collapse",)
    extra = 0
    # form
    autocomplete_fields = ("disciplines",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "discipline":
            program_internship_id = request.resolver_match.kwargs.get("object_id")

            if program_internship_id:
                program_internship = ProgramInternship.objects.get(id=program_internship_id)
                constraints = program_internship.get_discipline_constraints()
                # Update the discipline choices based on constraints
                kwargs["queryset"] = Discipline.objects.filter(id__in=constraints)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
