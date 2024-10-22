from ..form_builder.evaluations import FinalScoreStrategy
from .base import Evaluator


class GezbevEvaluator(Evaluator):
    """Evaluator for Gezbev."""

    education_code = "gezbev"
    default_scale = 45

    def get_scale(self) -> int:
        """Return the scale for the evaluation form."""
        return self.default_scale

    def evaluate(self) -> float | None:
        """Evaluate the model on the given data.

        :returns: A float representing the final score or None if it could not be calculated.
        """
        if not self.evaluation_form or not self.evaluation:
            return None

        scores = {score["value"]: score for score in self.evaluation_form.definition["scores"]}
        max_score = max([score["points"] for score in self.evaluation_form.definition["scores"] if score["points"]])

        # make a dict of the scores for easier access
        evaluation_scores = {}

        for section_code, section_data in self.evaluation.data["sections"].items():
            for item_code, item_data in section_data["scores"].items():
                evaluation_scores[(section_code, item_code)] = scores[item_data[0]]["points"]

        # go through the evaluation form and calculate the score
        # based on the final score strategy

        # FinalScoreStrategy.AVERAGE_ITEMS

        if self.evaluation_form.definition["final_score_strategy"] == FinalScoreStrategy.AVERAGE_ITEMS:
            # we calculate the score by summing the points and dividing by the maximum points possible
            # we then normalize the final result to the desired scale

            max_points = 0
            points = 0

            for section in self.evaluation_form.definition["sections"]:
                for item in section["items"]:
                    p = evaluation_scores.get((section["code"], item["value"]), None)

                    if p is not None:  # ignore 'nvt' scores
                        max_points += max_score
                        points += p

            return round((points / max_points) * self.get_scale(), 2)

        # FinalScoreStrategy.AVERAGE_SECTIONS_FIRST

        if self.evaluation_form.definition["final_score_strategy"] == FinalScoreStrategy.AVERAGE_SECTIONS_FIRST:
            # per section we sum the points, dividing by the maximum points and normalize to a 20 point scale
            # we then sum the section scores and normalize the final result to the desired scale

            section_scores = {}

            for section in self.evaluation_form.definition["sections"]:
                section_max_points = 0
                section_points = 0

                for item in section["items"]:
                    p = evaluation_scores.get((section["code"], item["value"]), None)

                    if p is not None:  # ignore 'nvt' scores
                        section_max_points += max_score
                        section_points += p

                section_scores[section["code"]] = round((section_points / section_max_points) * 20, 2)

            return round((sum(section_scores.values()) / (len(section_scores) * 20)) * self.get_scale(), 2)

        # default to None if the strategy is not implemented

        return None
