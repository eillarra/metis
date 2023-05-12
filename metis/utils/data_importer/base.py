import pandas as pd
import re

try:
    import phonenumbers
except ImportError:
    phonenumbers = None

from typing import Optional

from metis.models import User, Discipline, Region, Place, Education, TmpPlaceData
from metis.models.rel.addresses import Address
from metis.models.rel.remarks import Remark
from metis.services.mapbox import Mapbox, MapboxFeature


def get_or_create_place(education: Education, name: str, address: str) -> Place:
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

    place = Place.objects.create(education=education, name=name, code=name, region=region)

    if feature:
        Address.objects.create(
            content_object=place,
            address=feature.address,
            postcode=feature.postcode,
            city=feature.city,
            country=feature.country["short_code"] if feature.country else None,
        )

    return place


def get_or_create_user(*, name: str, email: Optional[str]) -> User:
    first_name, *last_name = name.split(None, 1)
    last_name = last_name[0] if last_name else "nan"
    username = f"{first_name}.{last_name}".lower().replace(" ", "")

    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email or f"{username}@ugent.be",
        )


def find_email_for_name(name: str, emails: list[str]) -> Optional[str]:
    for substring in name.lower().split():
        for email in emails:
            if substring in email.lower():
                return email
    return None


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
    return [format_phone_number(phone.strip()) for phone in re.split(r";|,\s|\s-\s| en | of | / ", str(phones))]


def parse_mentors(mentors: str) -> list[str]:
    return [mentor.strip() for mentor in re.split(r";|,\s|/", str(mentors))]


def df_to_places(df: pd.DataFrame, *, education: Education):
    df["phones"] = df["phones"].apply(parse_phones)
    df["mentors"] = df["mentors"].apply(parse_mentors)
    df["email"] = df["email"].apply(parse_emails)

    with Mapbox() as mapbox:
        df["feature"] = df["address"].apply(mapbox.geocode)

    # create a new place for each row
    for _, row in df.iterrows():
        place = get_or_create_place(education, str(row["name"]), str(row["address"]))

        # remarks
        if not pd.isna(row["remarks"]):
            Remark.objects.create(content_object=place, text=row["remarks"])

        # disciplines
        if row["discipline"]:
            discipline = Discipline.objects.get(code=row["discipline"])
            TmpPlaceData.objects.get_or_create(
                place=place,
                discipline=discipline,
                remarks=row["remarks"] if not pd.isna(row["remarks"]) else None,
            )

    return df
