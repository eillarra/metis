import pandas as pd
import re

try:
    import phonenumbers
except ImportError:
    phonenumbers = None

from django.db.utils import IntegrityError
from typing import Optional

from metis.models import Discipline, Region, Place, Project, ProjectPlace
from metis.models.rel.addresses import Address
from metis.models.rel.phone_numbers import PhoneNumber
from metis.models.rel.remarks import Remark
from metis.services.mapbox import Mapbox, MapboxFeature


def get_or_create_place(name: str, address: str) -> Place:
    try:
        return Place.objects.get(name=name)
    except Place.DoesNotExist:
        pass

    with Mapbox() as mapbox:
        feature: Optional[MapboxFeature] = mapbox.geocode(address)

    if not feature or not feature.region:
        region = None
    else:
        try:
            region = Region.objects.get(wikidata_id=feature.region["wikidata"])
        except Region.DoesNotExist:
            region = Region.objects.create(
                name_nl=feature.region["text_nl"],
                name_en=feature.region["text_en"],
                wikidata_id=feature.region["wikidata"],
                country=feature.country["short_code"] if feature.country else None,
            )

    place = Place.objects.create(name=name, region=region)

    if feature:
        Address.objects.create(
            content_object=place,
            address=feature.address,
            postcode=feature.postcode,
            city=feature.city,
            country=feature.country["short_code"] if feature.country else None,
        )

    return place


def format_phone_number(phone_number: str):
    try:
        return phonenumbers.format_number(
            phonenumbers.parse(phone_number, "BE"), phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
    except (phonenumbers.NumberParseException, TypeError):
        return phone_number


def parse_emails(emails: str) -> list[str]:
    return [emails.strip() for emails in re.split(r";|\s-\s| en | of | / ", str(emails))]


def parse_phones(phones: str) -> list[str]:
    return [format_phone_number(phone.strip()) for phone in re.split(r";|\s-\s| en | of | / ", str(phones))]


def parse_mentors(mentors: str) -> list[str]:
    return [mentor.strip() for mentor in re.split(r";|,\s|/", str(mentors))]


def df_to_places(df: pd.DataFrame, project: Optional[Project] = None):
    df["phones"] = df["phones"].apply(parse_phones)
    df["mentors"] = df["mentors"].apply(parse_mentors)

    with Mapbox() as mapbox:
        df["feature"] = df["address"].apply(mapbox.geocode)

    # create a new place for each row
    for _, row in df.iterrows():
        place = get_or_create_place(str(row["name"]), str(row["address"]))

        # contact information
        if row["phones"]:
            for phone in row["phones"]:
                PhoneNumber.objects.create(content_object=place, number=str(phone)[:22], type=PhoneNumber.LANDLINE)

        # disciplines

        # remarks

        if row["remarks"]:
            Remark.objects.create(content_object=place, text=row["remarks"])

        # add to project

        if project:
            try:
                pp = ProjectPlace.objects.create(project=project, place=place)
                pp.disciplines.add(Discipline.objects.get(code=row["discipline"]))
            except IntegrityError:
                pass

    return df
