import numpy as np
from scipy.optimize import linear_sum_assignment


def hungarian_optimizer(
    student_tops: list[tuple[int, list[int]]],
    project_place_availability: dict[int, int],
    preassigned_pairs: list[tuple[int, int]] | None = None,
) -> list[tuple[int, int, int]]:
    """
    Given a list of tuples with top project place choices for several students, a list of
    project_place availability and a list of predefined pairs, returns a list of tuples that
    maximizes the top choices.

    The function uses the Hungarian algorithm to optimize the matching of students and projects,
    with the constraint that the predefined pairs must be included in the result.

    Args:
        student_tops (list[tuple[int, list[int]]]): A list of tuples where the first element is the student_id
            and the second element the tops (project_place_ids), sorted by preference.
        project_place_availability (dict[int, int]): A dictionary with the project_place_id as key and the
            max availability as value.
        predefined_pairs (list[tuple[int, int]]): A list of pairs (student_id, project_place_id) that must be
            included in the final results.

    Returns:
        list[tuple[int, int, int]]: A list of tuples (student_id, project_place_id, rank) that maximizes
            the top choices, subject to the constraint that the predefined pairs are included in the result.
            The third element shows the rank of the project place in the student's top choices.
    """

    pairs = []

    # Create a list of students
    student_ids = [student_id for student_id, choices in student_tops if choices is not None]

    # If there are preassigned pairs, decrease the availability of the project place and remove the student
    if preassigned_pairs is not None:
        for student_id, project_place_id in preassigned_pairs:
            student_ids.remove(student_id)
            project_place_availability[project_place_id] -= 1
            if project_place_availability[project_place_id] <= 0:
                del project_place_availability[project_place_id]

    # Create a list of project places, duplicating those with more than one availability
    project_place_ids = [
        project_place_id
        for project_place_id, availability in project_place_availability.items()
        for _ in range(availability)
    ]

    # Create a cost matrix with a high default value
    cost_matrix = np.full((len(student_ids), len(project_place_ids)), np.inf)
    rank_matrix = np.full((len(student_ids), len(project_place_ids)), np.inf)

    # Fill in the cost matrix and rank matrix based on the students' top choices
    for student_id, choices in student_tops:
        if choices is None:
            continue
        if student_id in student_ids:
            for rank, project_place_id in enumerate(choices):
                if project_place_id not in project_place_availability:
                    continue
                i = student_ids.index(student_id)
                for j in range(project_place_ids.count(project_place_id)):
                    k = project_place_ids.index(project_place_id) + j
                    cost_matrix[i][k] = np.exp(rank)  # add a penalty for the rank
                    rank_matrix[i][k] = rank

    # Use the linear_sum_assignment function to find the optimal pairs
    row_idx, col_idx = linear_sum_assignment(cost_matrix)

    # Pair up the row and column indices into a list of tuples, and add the rank
    pairs = [
        (student_ids[i], project_place_ids[j], int(rank_matrix[i][j]) + 1)
        for i, j in zip(row_idx, col_idx, strict=True)
    ]

    # Add the preassigned pairs to the list of pairs
    if preassigned_pairs is not None:
        pairs.extend([(i, j, -1) for i, j in preassigned_pairs])

    return pairs
