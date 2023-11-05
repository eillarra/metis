import numpy as np
from scipy.optimize import linear_sum_assignment


def basic_hungarian_optimizer(
    tops: list[tuple[int, list[int]]],
    predefined_pairs: list[tuple[int, int]] | None = None,
    penalty: float = 0.01,
) -> list[tuple[int, int, int]]:
    """
    Given a list of tuples with top project place choices for several students, and a list of predefined pairs,
    returns a list of tuples that maximizes the top choices.

    The function uses the Hungarian algorithm to optimize the matching of students and projects,
    with the constraint that the predefined pairs must be included in the result.

    Args:
        tops (list[tuple[int, list[int]]]): A list of tuples where the first element is the student_id
            and the second element the tops (project_place_ids), sorted by preference.
        predefined_pairs (list[tuple[int, int]]): A list of pairs (student_id, project_place_id) that must be
            included in the final results.

    Returns:
        list[tuple[int, int, int]]: A list of tuples (student_id, project_place_id, rank) that maximizes
            the top choices, subject to the constraint that the predefined pairs are included in the result.
            The third element shows the rank of the project place in the student's top choices.
    """

    # If no predefined pairs are given, set predefined_pairs to an empty list
    if predefined_pairs is None:
        predefined_pairs = []

    # Remove the students in predefined_pairs from tops
    predefined_student_ids = {student_id for student_id, _ in predefined_pairs}
    tops = [(student_id, choices) for student_id, choices in tops if student_id not in predefined_student_ids]

    # Remove the students and project_places in predefined_pairs from tops
    tops_dict = {student_id: choices for student_id, choices in tops}
    for student_id, project_place_id in predefined_pairs:
        if student_id in tops_dict:
            del tops_dict[student_id]
        for choices in tops_dict.values():
            if project_place_id in choices:
                choices.remove(project_place_id)

    # Create a mapping from student/project_place IDs to indices
    student_ids = [student_id for student_id, _ in tops]
    project_place_ids = sorted(set(id for choices in tops_dict.values() for id in choices))

    # Create a matrix of costs with a high default value
    cost_matrix = np.full((len(student_ids), len(project_place_ids)), np.inf)

    # Create a dictionary to store the ranks
    ranks = {}

    # Fill in the cost matrix based on the students' top choices
    for idx, (student_id, choices) in enumerate(tops):
        for rank, project_place_id in enumerate(choices):
            if project_place_id not in project_place_ids:  # Skip if the project_place_id is not in the list
                continue
            i = student_ids.index(student_id)
            j = project_place_ids.index(project_place_id)
            cost_matrix[i][j] = rank + idx * penalty  # Add a small penalty based on the order
            ranks[(student_id, project_place_id)] = rank + 1

    # Use the linear_sum_assignment function to find the optimal pairs
    row_indices, col_indices = linear_sum_assignment(cost_matrix)

    # Pair up the row and column indices into a list of tuples, and add the rank
    results = [
        (student_ids[i], project_place_ids[j], ranks.get((student_ids[i], project_place_ids[j]), -1))
        for i, j in zip(row_indices, col_indices, strict=True)
    ]

    # Add the predefined pairs back to the list of pairs, with a rank of -1
    results.extend((student_id, project_id, -1) for student_id, project_id in predefined_pairs)

    return results
