def find_students_for_places(
    student_tops: list[tuple[int, list[int]]],
    project_places: list[int],
) -> dict[int, list[int]]:
    """Given some student tops, return, per project_place_id, a list of students ordered by rank (or empty list).

    Args:
        student_tops: A list of tuples (student_id, top_choices) where top_choices is a list of project_place_ids
        project_places: A list of project_place_ids

    Returns:
        A dictionary of project_place_id: list(student_id)
    """
    choices = {}

    for project_place_id in project_places:
        choices.setdefault(project_place_id, [])

        for student_id, top_choices in student_tops:
            if top_choices is None:
                continue
            if project_place_id in top_choices:
                choices[project_place_id].append((student_id, top_choices.index(project_place_id)))

    # sort by rank and get rid of the rank
    for project_place_id in project_places:
        choices[project_place_id] = sorted(choices[project_place_id], key=lambda x: x[1])
        choices[project_place_id] = [x[0] for x in choices[project_place_id]]

    return choices
