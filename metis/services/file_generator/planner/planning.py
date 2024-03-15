from datetime import datetime

import pandas as pd
from django.utils.text import slugify
from pydantic import BaseModel

from metis.models import ProjectPlaceAvailability, Questioning
from metis.services.planner.hungarian import hungarian_optimizer
from metis.services.planner.utils import find_students_for_places

from ..excel import Excel, ExcelSheet


class PlanningExcelOptions(BaseModel):
    """Options for the PlanningExcel class."""

    students_with_first_choice: list[int] | None = None
    students_to_skip: list[int] | None = None
    places_with_students: list[int] | None = None
    places_to_skip: list[int] | None = None


class PlanningExcel(Excel):
    """Generate an Excel file with a planning proposal."""

    def __init__(self, questioning: Questioning, *, options: dict | None = None):
        self.questioning = questioning
        self.options = PlanningExcelOptions(**options or {})
        self._process_data()

    def _process_data(self):
        questioning = self.questioning
        project_places_with_availability = questioning.project.project_places.filter(
            availability_set__period=questioning.period, availability_set__min__gt=0
        )
        target_places = project_places_with_availability.exclude(id__in=self.options.places_to_skip or [])
        target_student_ids = set(questioning.get_target_group().values_list("id", flat=True))

        # check if there are places of students to skip, based on options
        # places were already filtered on `target_places`
        if self.options.students_to_skip is not None:
            for student_id in self.options.students_to_skip:
                if student_id not in target_student_ids:
                    raise ValueError(f"Student with id {student_id} not found in tops")
                target_student_ids.remove(student_id)

        # work the data
        availabilities = {
            a.project_place_id: a.max  # type: ignore
            for a in ProjectPlaceAvailability.objects.filter(period=questioning.period)
        }
        student_tops = [
            (response.object_id, response.data["tops"])
            for response in questioning.responses.all()
            if response.data["tops"] is not None and response.object_id in target_student_ids
        ]
        project_place_availability = {
            project_place.id: availabilities[project_place.id] for project_place in project_places_with_availability
        }
        student_tops_dict = {student_id: tops for student_id, tops in student_tops}

        # check if there are preassigned pairs, based on options
        preassigned_pairs = []
        preassigned_students = set()

        if self.options.students_with_first_choice is not None:
            for student_id in self.options.students_with_first_choice:
                student_id = int(student_id)
                if student_id not in student_tops_dict:
                    raise ValueError(f"Student with id {student_id} not found in tops")
                preassigned_pairs.append((student_id, student_tops_dict[student_id][0]))
                preassigned_students.add(student_id)

        if self.options.places_with_students is not None:
            top_students_for_places = find_students_for_places(student_tops, self.options.places_with_students)
            for place_id, student_ids in top_students_for_places.items():
                for student_id in student_ids:
                    if student_id in preassigned_students:
                        continue
                    preassigned_pairs.append((student_id, place_id))
                    preassigned_students.add(student_id)
                    break

        planning = hungarian_optimizer(
            student_tops, project_place_availability, preassigned_pairs, self.questioning.random_seed
        )

        # massage the data, with real project place names and student names
        for idx, (student_id, project_place_id, rank, preassigned) in enumerate(planning):
            planning[idx] = (
                questioning.get_target_group().get(id=student_id),
                questioning.project.project_places.get(id=project_place_id),
                rank,
                preassigned,
            )

        # sort the planning by student name
        self.planning = sorted(planning, key=lambda x: x[0].reverse_name)

        # make a list of all places, with the assigned students
        places_with_students = {}
        for student, place, _, _ in planning:
            places_with_students.setdefault(place, []).append(student)

        # make a full list of places
        self.list_of_places = []
        for target_place in target_places:
            self.list_of_places.append(
                (target_place, len(places_with_students.get(target_place, [])), availabilities[target_place.id])
            )

        # sort the full list of places by name
        self.list_of_places = sorted(self.list_of_places, key=lambda x: x[0].place.name)

        # set some attributes
        self.created_at = datetime.now()
        self.ranks = {}

        for _, _, rank, _ in planning:
            self.ranks[rank] = self.ranks.get(rank, 0) + 1

        self.ranks = dict(sorted(self.ranks.items()))

    def get_filename(self) -> str:
        """Get the filename of the Excel file, without extension."""
        filename = "_".join(
            [
                "metis",
                self.questioning.project.education.code,
                self.questioning.project.name,
                self.questioning.period.full_name if self.questioning.period else "",
                "planning",
                str(self.questioning.random_seed or ""),
            ]
        )
        return slugify(filename)

    def get_sheets(self) -> list[ExcelSheet]:
        """Generate an Excel file with all the responses of a questioning, based on type."""
        from ..questionings.student_tops import get_student_tops_sheets

        return [
            self.get_planning_sheet(),
            self.get_place_distribution_sheet(),
            get_student_tops_sheets(self.questioning)[0],
            self.get_configuration_sheet(),
        ]

    def get_configuration_sheet(self) -> ExcelSheet:
        """Generate an Excel sheet with the configuration of the questioning."""
        df = pd.DataFrame(
            [
                ["created_at", str(self.created_at)],
                ["period", self.questioning.period.full_name if self.questioning.period else ""],
                ["questioning", self.questioning.title],
                ["type", self.questioning.type],
                ["random_seed", str(self.questioning.random_seed)],
                ["s_first", ",".join([str(id) for id in self.options.students_with_first_choice or ["-"]])],
                ["s_skip", ",".join([str(id) for id in self.options.students_to_skip or ["-"]])],
                ["p_force", ",".join([str(id) for id in self.options.places_with_students or ["-"]])],
                ["p_skip", ",".join([str(id) for id in self.options.places_to_skip or ["-"]])],
            ],
            columns=["key", "value"],
        )
        df = df.set_index(["key"])

        return ExcelSheet(name="Configuration", df=df)

    def get_planning_sheet(self) -> ExcelSheet:
        """Generate an Excel sheet with the planning proposal."""
        columns = ["student_id", "student", "place", "top", "preassigned"]
        rows = []

        for student, project_place, top, preassigned in self.planning:
            rows.append([student.id, student.reverse_name, project_place.name, top, preassigned])

        df = pd.DataFrame(rows, columns=columns)
        df = df.set_index(["student_id"])

        return ExcelSheet(name="Planning", df=df)

    def get_place_distribution_sheet(self) -> ExcelSheet:
        """Generate an Excel sheet with the place distribution."""
        columns = ["place_id", "place", "availability", "students"]
        rows = []

        for project_place, assigned_places, availability in self.list_of_places:
            rows.append([project_place.id, project_place.place.name, availability, assigned_places])

        df = pd.DataFrame(rows, columns=columns)
        df = df.set_index(["place_id"])

        return ExcelSheet(name="Places", df=df)
