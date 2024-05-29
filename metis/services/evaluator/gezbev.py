from .base import Evaluator


class GezbevEvaluator(Evaluator):
    """Evaluator for Gezbev."""

    education_code = "gezbev"

    def evaluate(self) -> float | None:
        """Evaluate the model on the given data.

        We calculate how many items we have to evaluate.
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

        # make a dict of the scores for easier access
        evaluation_scores = {}

        for section_code, section_data in self.evaluation.data["sections"].items():
            for item_code, item_data in section_data["scores"].items():
                evaluation_scores[(section_code, item_code)] = scores[item_data[0]]["points"]

        # go through the evaluation form and calculate the score

        for section in self.evaluation_form.definition["sections"]:
            for item in section["items"]:
                p = evaluation_scores.get((section["code"], item["value"]), None)

                if p is not None:  # ignore 'nvt' scores
                    max_points += max_score
                    points += p

        return round((points / max_points) * 45, 2)
