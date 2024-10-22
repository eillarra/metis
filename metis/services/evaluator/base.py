from metis.models.stages import Evaluation, Internship


class Evaluator:
    """Base class for an Evaluator.

    It takes an internship and evaluates it based on the given data.

    :param internship: The internship to evaluate.
    """

    def __init__(self, internship: Internship):
        self.internship = internship
        self.evaluation_form = internship.evaluation_form

        try:
            self.evaluation = Evaluation.objects.get(
                internship=internship, intermediate=0, is_approved=True, is_self_evaluation=False
            )
        except Evaluation.DoesNotExist:
            self.evaluation = None

    def evaluate(self) -> float | None:
        """Evaluate the model on the given data.

        By default the result of the global score of the final evaluation will be returned.

        :returns: A float representing the final score or None if it could not be calculated.
        """
        if not self.evaluation_form or not self.evaluation:
            return None

        scores = {score["value"]: score for score in self.evaluation_form.definition["scores"]}
        return scores[self.evaluation.data["global_score"]]["points"]


def get_evaluator(internship: Internship) -> Evaluator:
    """Get an evaluator for the given evaluation."""
    from .gezbev import GezbevEvaluator

    education_code = internship.education.code

    if education_code == GezbevEvaluator.education_code:
        return GezbevEvaluator(internship)

    return Evaluator(internship)
