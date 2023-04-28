import pandas as pd

from django.db.utils import IntegrityError
from django.utils.text import slugify
from typing import Optional

from metis.models import ProgramBlock, Project, ProjectPlace, Student, User
from metis.models.tmp.stages import TmpStudent, TmpMentor, TmpInternship
from .base import parse_emails, parse_phones, parse_mentors, get_or_create_place, df_to_places


def find_email_for_name(name: str, emails: list[str]) -> Optional[str]:
    for substring in name.lower().split():
        for email in emails:
            if substring in email.lower():
                return email
    return None


def load_places(*, project: Optional[Project] = None):
    file_path = "metis/utils/data_importer/files/Stageplaatsen_audiologie_AJ22-23.xlsx"
    df = pd.read_excel(file_path, sheet_name="Overzicht stageplaatsen", nrows=230)
    df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # rename columns to match the Place model
    df.rename(
        columns={
            "Naam": "name",
            "Adres": "address",
            "Telefoon": "phones",
            "E-mailadres": "email",
            "Regio": "region",
            "Type stageplaats": "discipline",
            "Stagementoren": "mentors",
            "Bereikbaarheid": "accessibility",
            "Datum toezegging": "date_of_acceptance",
            "Opmerkingen": "remarks",
        },
        inplace=True,
    )

    return df_to_places(df, project=project)


def load_internships(audio_periods, *, education):
    for data in audio_periods:
        file_path = "metis/utils/data_importer/files/verdeling_stageplaatsen_audiologie.xlsx"
        df = pd.read_excel(file_path, sheet_name=f"{data.project_name}-{data.block_name}-Periode{data.period}")

        df.rename(
            columns={
                "Student": "student_name",
                "Stageplaats": "place_name",
                "Stagementoren": "mentors",
                "Adres": "place_adress",
                "Telefoon": "mentor_phone_numbers",
                "E-mailadres": "mentor_emails",
                "Opmerkingen": "remarks",
            },
            inplace=True,
        )

        df["mentors"] = df["mentors"].apply(parse_mentors)
        df["mentor_emails"] = df["mentor_emails"].apply(parse_emails)
        df["mentor_phone_numbers"] = df["mentor_phone_numbers"].apply(parse_phones)
        df["place"] = df.apply(
            lambda row: get_or_create_place(str(row["place_name"]), str(row["place_adress"])), axis=1
        )

        # link place to project

        project = Project.objects.get(name=data.project_name)
        block = ProgramBlock.objects.get(program__education=education, name=data.block_name)

        if data.link_places:
            for place in df["place"]:
                try:
                    ProjectPlace.objects.create(project=project, place=place)
                except IntegrityError:
                    pass

        # create temp tables

        print(f"Number of rows in df: {len(df)} for {data.project_name}-{data.block_name}-Periode{data.period}")

        for _, row in df.iterrows():
            student, _ = TmpStudent.objects.get_or_create(
                project=project,
                block=block,
                name=str(row["student_name"]).strip(),
                period=data.period,
            )

            internship, _ = TmpInternship.objects.get_or_create(
                project=project,
                place=row["place"],
                student=student,
                project_name=data.project_name,
                block_name=data.block_name,
                period=data.period,
            )

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

    for tmp_student in TmpStudent.objects.all():
        first_name, *last_name = tmp_student.name.split(None, 1)
        last_name = last_name[0] if last_name else "?"

        user, _ = User.objects.get_or_create(
            username=slugify(f"{first_name}.{last_name}"),
            first_name=first_name,
            last_name=last_name,
            email=tmp_student.email or "noreply@ugent.be",
        )
        student, _ = Student.objects.get_or_create(
            user=user,
            project=tmp_student.project,
            block=tmp_student.block,
        )
