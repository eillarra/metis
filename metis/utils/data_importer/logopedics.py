import pandas as pd

from typing import Optional

from metis.models import Project
from .base import df_to_places


def load_places(*, project: Optional[Project] = None):
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

    return df_to_places(df, project=project)
