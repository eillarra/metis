from django.core.management.base import BaseCommand

from metis.models.stages import Questioning
from metis.services.planner.hungarian import basic_hungarian_optimizer


class Command(BaseCommand):
    """Run the Hungarian algorithm to optimize the planning of stages.

    :usage:
    >>> python manage.py hungarian <questioning_id>
    """

    def add_arguments(self, parser):
        parser.add_argument("questioning_id", type=int)

    def handle(self, *args, **options):
        questioning = Questioning.objects.get(id=options["questioning_id"])
        if questioning.type != Questioning.STUDENT_TOPS:
            raise ValueError(f"Invalid type: {questioning.type}")

        student_tops = [(response.object_id, response.data["tops"]) for response in questioning.responses.all()]
        planning = basic_hungarian_optimizer(student_tops)

        # print results

        print(planning)

        # print the number of responses per ranks

        ranks = {}
        for _, _, rank in planning:
            ranks[rank] = ranks.get(rank, 0) + 1
        ranks = dict(sorted(ranks.items()))
        print(ranks)
