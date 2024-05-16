from .base import Evaluator


class GezbevEvaluator(Evaluator):
    """Evaluator for Gezbev."""

    education_code = "gezbev"

    def evaluate(self) -> float | None:
        """Evaluate the model on the given data.

        We calculate how many items we have to evaluate.
        TODO: do we ignore the nvt answers?
        We assign the maximun score to each item, so we know the maximum score possible.
        We calculate the final score by dividing the sum of the scores by the maximum score,
        and normalizing the result to a 45 point scale.

        :return: A float representing the final score or None if it could not be calculated.
        """
        if not self.evaluation_form or not self.evaluation:
            return None

        scores = {score["value"]: score for score in self.evaluation_form.definition["scores"]}
        max_score = max([score["points"] for score in self.evaluation_form.definition["scores"] if score["points"]])
        max_points = 0
        points = 0

        for _, section_data in self.evaluation.data["sections"].items():
            for _, item_data in section_data["scores"].items():
                max_points += max_score
                p = scores[item_data[0]]["points"]
                points += p if p else 0

        return round((points / max_points) * 45, 2)
