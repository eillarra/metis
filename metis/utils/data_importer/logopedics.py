import datetime
import pandas as pd

from typing import Dict, Tuple

from metis.models import (
    Track,
    ProgramBlock,
    Project,
    ProjectPlace,
    ProjectPlace,
    Period,
    Student,
    Contact,
    Remark,
    Internship,
    ProgramInternship,
    Discipline,
)
from metis.models.tmp.stages import TmpStudent, TmpMentor, TmpInternship, TmpPlaceData
from .base import (
    df_to_places,
    find_email_for_name,
    get_or_create_place,
    get_or_create_user,
    parse_emails,
    parse_phones,
    parse_mentors,
)


def load_places(project: Project):
    file_path = "metis/utils/data_importer/files/Stageplaatsen_logopedie_AJ22-23.xlsx"
    df = pd.read_excel(file_path, sheet_name="Blad1", nrows=263)

    # rename columns to match the Place model
    df.rename(
        columns={
            "STAGEPLAATSEN IN VLAANDEREN": "name",
            "VERANTWOORDELIJKE": "mentors",
            "E-MAIL": "email",
            "Opmerkingen": "remarks",
        },
        inplace=True,
    )

    # add columns to match the Place model
    df["address"] = df["STRAAT+NUMMER"] + ", " + df["PLAATS"]
    df["phones"] = df["TEL"] + " / " + df["GSM"]
    df["discipline"] = "logopedie"

    return df_to_places(df, education=project.education)


def load_internships(audio_periods, *, education):
    for data in audio_periods:
        file_path = "metis/utils/data_importer/files/verdeling_stageplaatsen_logopedie.xlsx"
        df = pd.read_excel(file_path, sheet_name=f"{data.project_name}-{data.block_name}-Periode{data.period}")

        # rename columns
        df.rename(
            columns={
                "Student": "student_name",
                "E-mail student": "student_email",
                "Stageplaats": "place_name",
                "Stagementoren": "mentors",
                "Adres": "place_adress",
                "Telefoon": "mentor_phone_numbers",
                "E-mailadres": "mentor_emails",
                "Opmerkingen": "remarks",
            },
            inplace=True,
        )

        # strip whitespace
        df["student_name"] = df["student_name"].str.strip()
        df["student_email"] = df["student_email"].str.strip()
        df["place_name"] = df["place_name"].str.strip()

        # transform data
        if "mentors" in df.columns:
            df["mentors"] = df["mentors"].apply(parse_mentors)
        if "mentor_emails" in df.columns:
            df["mentor_emails"] = df["mentor_emails"].apply(parse_emails)
        if "mentor_phone_numbers" in df.columns:
            df["mentor_phone_numbers"] = df["mentor_phone_numbers"].apply(parse_phones)

        if "place_adress" in df.columns:
            df["place"] = df.apply(
                lambda row: get_or_create_place(
                    education=education,
                    name=row["place_name"],
                    address=str(row["place_adress"]),
                ),
                axis=1,
            )
        else:
            df["place"] = df.apply(
                lambda row: get_or_create_place(
                    education=education,
                    name=row["place_name"],
                ),
                axis=1,
            )

        # link place to project

        project = Project.objects.get(education=education, name=data.project_name)
        block = ProgramBlock.objects.get(program__education=education, name=data.block_name)

        # create tmp tables

        print(f"Number of rows in df: {len(df)} for {data.project_name}-{data.block_name}-Periode{data.period}")

        for _, row in df.iterrows():
            student_email = str(row["student_email"]).strip().lower()

            student, _ = TmpStudent.objects.get_or_create(
                project=project,
                block=block,
                name=str(row["student_name"]).strip(),
                email=str(row["student_email"]).strip().lower(),
                period=data.period,
            )

            internship, _ = TmpInternship.objects.get_or_create(
                project=project,
                place=row["place"],
                student=student if student_email != "nan" else None,
                project_name=data.project_name,
                block_name=data.block_name,
                period=data.period,
            )

            if "mentors" in df.columns:
                for mentor_name in row["mentors"]:
                    """
                    Find some match for the mentor name in the emails.
                    """
                    email = find_email_for_name(mentor_name, row["mentor_emails"]) or row["mentor_emails"][0]

                    try:
                        mentor = TmpMentor.objects.get(name=mentor_name)
                    except TmpMentor.DoesNotExist:
                        mentor = TmpMentor.objects.create(
                            project=project,
                            place=row["place"],
                            name=mentor_name,
                            email=email.lower(),
                            address=row["place_adress"],
                            phone_numbers=row["mentor_phone_numbers"],
                            emails=",".join(row["mentor_emails"]),
                        )

                    internship.mentors.add(mentor)

    # move data to the real tables

    tmp_students_map = {}

    for tmp_student in TmpStudent.objects.filter(project__education=education):
        if tmp_student.email != "nan":
            user = get_or_create_user(name=tmp_student.name, email=tmp_student.email)
            student, _ = Student.objects.get_or_create(
                user=user,
                project=tmp_student.project,
                block=tmp_student.block,
            )
            tmp_students_map[tmp_student.id] = student

    for tmp_mentor in TmpMentor.objects.filter(project__education=education):
        user = get_or_create_user(name=tmp_mentor.name, email=tmp_mentor.email)

        Contact.objects.get_or_create(
            user=user,
            place=tmp_mentor.place,
            is_mentor=True,
        )

        proj_place, _ = ProjectPlace.objects.get_or_create(project=tmp_mentor.project, place=tmp_mentor.place)

        try:
            tmp_place_data = TmpPlaceData.objects.get(place=tmp_mentor.place)
            if tmp_place_data.discipline:
                proj_place.disciplines.add(tmp_place_data.discipline)
            if tmp_place_data.remarks:
                Remark.objects.create(content_object=tmp_mentor.place, text=tmp_place_data.remarks)
        except TmpPlaceData.DoesNotExist:
            pass

    for internship in TmpInternship.objects.filter(project__education=education):
        naming_map: Dict[Tuple[str, str], str] = {
            ("Ba3", "1"): "1A",
            ("Ma1", "1"): "2A",
            ("Ma2", "1"): "3A",
        }

        proj_place, _ = ProjectPlace.objects.get_or_create(project=internship.project, place=internship.place)
        default_discipline = Discipline.objects.get(education=education, name="logopedie")

        period, _ = Period.objects.get_or_create(
            project=internship.project,
            program_internship=ProgramInternship.objects.get(
                block__program__education=education,
                block__name=internship.block_name,
                name__contains=naming_map[(internship.block_name, internship.period)],
            ),
            name=internship.period,
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2024, 1, 1),
        )

        internship = Internship(
            project=internship.project,
            student=tmp_students_map[internship.student.id] if internship.student else None,
            project_place=proj_place,
            period=period,
            track=Track.objects.get(program__education=education, name="Track A"),
            discipline=default_discipline,
        )
        internship.clean()
        internship.save()
