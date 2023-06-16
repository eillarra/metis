from metis.models import Project


def clone_project(project: Project, name: str) -> Project:
    """
    Clone a project with a new name.
    When cloning the project, import:
    - project's periods with new dates in the future (next year)
    - project's places
    - projects students, if they are not already at the end of their tracks (check block position for this)
    """

    """
    TODO: clone related placeforms, studentforms
    """

    new_project = Project.objects.get(pk=project.pk)
    new_project.name = name
    new_project.pk = None
    new_project.save()

    for period in project.periods.all():
        period.pk = None
        period.project = new_project
        period.start_date = period.start_date.replace(year=period.start_date.year + 1)
        period.end_date = period.end_date.replace(year=period.end_date.year + 1)
        period.save()

    for project_place in project.place_set.all():
        disciplines = project_place.disciplines.all()
        availability_set = project_place.availability_set.all()
        project_place.pk = None
        project_place.project = new_project
        project_place.save()

        for discipline in disciplines:
            project_place.disciplines.add(discipline)

        for availability in availability_set:
            period = availability.period
            availability.pk = None
            availability.period = new_project.periods.get(
                program_internship=period.program_internship, name=period.name
            )
            availability.place = project_place
            availability.save()

    last_block = project.program.blocks.last()

    for student in project.students.all():
        if student.block.position is not last_block.position:
            student.pk = None
            student.project = new_project
            student.block = (
                new_project.program.blocks.get(position=student.block.position + 1) if student.block else None
            )
            student.save()

    return new_project
