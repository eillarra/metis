from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest, PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from metis.services.file_generator.excel import QuestioningExcel
from metis.models import ProjectPlaceAvailability, Questioning
from metis.services.file_generator.pdf import render_pdf_template
from metis.services.planner.hungarian import hungarian_optimizer
from metis.services.planner.utils import find_students_for_places


class QuestioningFileView(View):
    template_name = "pdfs/questioning.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().project.can_be_managed_by(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Questioning:
        if not hasattr(self, "object"):
            self.object = get_object_or_404(Questioning, id=self.kwargs.get("questioning_id"))
        return self.object

    def get(self, request, *args, **kwargs):
        context = {"questioning": self.get_object()}
        file_type = self.kwargs.get("file_type")

        if file_type == "pdf":
            return render_pdf_template(request, self.template_name, context)
        elif file_type == "xlsx":
            return QuestioningExcel(self.get_object()).get_response()
        else:
            raise BadRequest("Invalid file type")


class PlanningFileView(QuestioningFileView):
    template_name = "pdfs/planning.html"

    def get(self, request, *args, **kwargs):
        questioning = self.get_object()
        target_places = questioning.project.project_places.filter(
            availability_set__period=questioning.period, availability_set__min__gt=0
        )
        target_student_ids = questioning.get_target_group().values_list("id", flat=True)

        availabilities = {
            a.project_place_id: a.max for a in ProjectPlaceAvailability.objects.filter(period=questioning.period)
        }
        student_tops = [
            (response.object_id, response.data["tops"])
            for response in questioning.responses.all()
            if response.data["tops"] is not None and response.object_id in target_student_ids
        ]
        project_place_availability = {
            project_place.id: availabilities[project_place.id] for project_place in target_places
        }
        student_tops_dict = {student_id: tops for student_id, tops in student_tops}

        # check if there are preassigned pairs
        # two query parameters can be set: students_first_choice, and places_with_students
        # both are comma-separated lists of student ids and project_place ids respectively

        preassigned_pairs = []

        students_first_choice = request.GET.get("students_first_choice")
        places_with_students = request.GET.get("places_with_students")
        preassigned_students = set()

        if students_first_choice is not None:
            students_first_choice = [int(id) for id in students_first_choice.split(",")]
            for student_id in students_first_choice:
                student_id = int(student_id)
                if student_id not in student_tops_dict:
                    raise BadRequest(f"Student with id {student_id} not found in tops")
                preassigned_pairs.append((student_id, student_tops_dict[student_id][0]))
                preassigned_students.add(student_id)

        if places_with_students is not None:
            places_with_students = [int(id) for id in places_with_students.split(",")]
            top_students_for_places = find_students_for_places(student_tops, places_with_students)
            for place_id, student_ids in top_students_for_places.items():
                for student_id in student_ids:
                    if student_id in preassigned_students:
                        continue
                    preassigned_pairs.append((student_id, place_id))
                    preassigned_students.add(student_id)
                    break

        planning = hungarian_optimizer(student_tops, project_place_availability, preassigned_pairs)

        ranks = {}
        for _, _, rank in planning:
            ranks[rank] = ranks.get(rank, 0) + 1
        ranks = dict(sorted(ranks.items()))

        # massage the data, with real project place names and student names
        for idx, (student_id, project_place_id, rank) in enumerate(planning):
            planning[idx] = (
                questioning.get_target_group().get(id=student_id),
                questioning.project.project_places.get(id=project_place_id),
                rank,
            )

        # sort the planning by student name
        planning = sorted(planning, key=lambda x: x[0].user.name)

        # make a list of all places, with the assigned students
        places_with_students = {}
        for student, place, _ in planning:
            places_with_students.setdefault(place, []).append(student)

        # make a full list of places
        full_list_of_places = []
        for target_place in target_places:
            full_list_of_places.append(
                (target_place, len(places_with_students.get(target_place, [])), availabilities[target_place.id])
            )

        # sort the full list of places by name
        full_list_of_places = sorted(full_list_of_places, key=lambda x: x[0].place.name)

        context = {
            "questioning": questioning,
            "planning": planning,
            "ranks": ranks,
            "full_list_of_places": full_list_of_places,
        }

        return render_pdf_template(request, self.template_name, context)
