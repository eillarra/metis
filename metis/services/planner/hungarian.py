from random import Random

import numpy as np
from scipy.optimize import linear_sum_assignment


def hungarian_optimizer(
    student_tops: list[tuple[int, list[int]]],
    project_place_availability: dict[int, int],
    preassigned_pairs: list[tuple[int, int]] | None = None,
    seed: int | None = None,
) -> list[tuple[int, int, int, bool]]:
    """Hungarian algorithm for optimizing the matching of students and project places.

    Args:
        student_tops: A list of tuples (student_id, top_choices) where top_choices is a list of project_place_ids
        project_place_availability: A dictionary of project_place_id: availability pairs, where availability is the
            max number of students that can be matched to the project place.
        preassigned_pairs: A list of tuples (student_id, project_place_id) that must be included in the result.
        seed: A seed for the randomizer.

    Returns:
        An optimized list of tuples (student_id, project_place_id, rank, preassigned) where rank is the rank
        of the project place (top) in the student's top choices, or -1 if the student was preassigned
        to the project place.
    """
    pairs = []

    if seed:
        randomizer = Random(seed)
        randomizer.shuffle(student_tops)

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
                for j in range(project_place_availability[project_place_id]):
                    k = project_place_ids.index(project_place_id) + j
                    cost_matrix[i][k] = np.exp(rank)  # add a penalty for the rank
                    rank_matrix[i][k] = rank

    # Use the linear_sum_assignment function to find the optimal pairs
    row_idx, col_idx = linear_sum_assignment(cost_matrix)

    # Pair up the row and column indices into a list of tuples, and add the rank
    pairs = [
        (int(student_ids[i]), int(project_place_ids[j]), int(rank_matrix[i][j]) + 1, bool(0))  # type hack
        for i, j in zip(row_idx, col_idx, strict=True)
    ]

    # Add the preassigned pairs to the list of pairs
    if preassigned_pairs is not None:
        student_tops_dict = {}
        for student_id, choices in student_tops:
            if choices is None:
                continue
            for rank, project_place_id in enumerate(choices):
                student_tops_dict[(student_id, project_place_id)] = int(rank + 1)

        for i, j in preassigned_pairs:
            pairs.append((i, j, student_tops_dict[(i, j)], True))

    return pairs
