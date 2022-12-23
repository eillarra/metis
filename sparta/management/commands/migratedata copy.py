from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy import create_engine
from typing import Optional
from zoneinfo import ZoneInfo

from sparta.models import (
    Faculty,
    Education,
    Discipline,
    Project,
)


TZ = ZoneInfo("Europe/Brussels")
User = get_user_model()


def make_dt_aware(naive: datetime) -> Optional[datetime]:
    try:
        aware = make_aware(naive, timezone=TZ)
    except KeyError:
        aware = TZ.localize(naive, is_dst=False)
    except Exception:
        aware = None

    return aware


def get_base_fields(obj, prefix: str) -> dict:
    return {
        "is_active": getattr(obj, f"{prefix}IsActive"),
        "position": getattr(obj, f"{prefix}OrderNumber"),
        "created_at": make_dt_aware(getattr(obj, f"{prefix}InsertDate")),
        # "created_by_id": obj.get(f"{prefix}LastChangeAccountId"),
        "updated_at": make_dt_aware(getattr(obj, f"{prefix}LastChangeDate")),
        # "updated_by_id": obj.get(f"{prefix}LastChangeAccountId"),
    }


class Command(BaseCommand):
    help = "Migrates legacy SPARTA database to new tables."

    def automap_all_tables(self, uri):
        """http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html"""
        Base = automap_base()
        engine = create_engine(uri)
        Base.prepare(engine, reflect=True)

        return Base, OrmSession(engine)

    @staticmethod
    def batch(iterable, n=1):
        size = len(iterable)
        for idx in range(0, size, n):
            yield iterable[idx : min(idx + n, size)]

    def out(self, msg_type: str, msg: str):
        if msg_type == "info":
            return self.stdout.write(self.style.MIGRATE_HEADING(msg))
        if msg_type == "success":
            return self.stdout.write(self.style.SUCCESS(msg))
        else:
            return self.stdout.write(msg)

    def handle(self, *args, **options):
        CONNECTION_URI = "mysql://root@127.0.0.1:3306/sparta_old"
        Base, session = self.automap_all_tables(CONNECTION_URI)

        # Update Site info

        self.out("info", "Let's start!")

        site = Site.objects.get(pk=1)
        site.domain = "sparta.ugent.be"
        site.name = "SPARTA"
        site.save()

        # ------
        # Places
        # ------

        """
        self.out("info", "Migrating places...")
        regions_dict = {}
        region_names_dict = {}

        for obj in session.query(Base.classes.TrainingRegion).all():
            if obj.TrainingRegionName in region_names_dict:
                regions_dict[obj.TrainingRegionID] = region_names_dict[obj.TrainingRegionName]
                continue

            Region.objects.create(
                id=obj.TrainingRegionID,
                is_active=obj.TrainingRegionIsActive,
                is_visible_for_students=obj.TrainingRegionIsVisibleForStudent,
                name=obj.TrainingRegionName,
                created_at=make_dt_aware(obj.TrainingRegionInsertDate),
                updated_at=make_dt_aware(obj.TrainingRegionLastChangeDate),
            )

            regions_dict[obj.TrainingRegionID] = obj.TrainingRegionID
            region_names_dict[obj.TrainingRegionName] = obj.TrainingRegionID

        self.out("success", f"✔ Regions migrated! ({Region.objects.count()} records)")

        for obj in session.query(Base.classes.TrainingPlace).all():
            if obj.TrainingPlaceParentPlaceID and obj.TrainingPlaceParentPlaceID > 0:
                continue

            region_id = (
                obj.TrainingPlaceTrainingRegionID
                if (obj.TrainingPlaceTrainingRegionID and obj.TrainingPlaceTrainingRegionID > 0)
                else None
            )

            TrainingPlace.objects.create(
                id=obj.TrainingPlaceID,
                is_active=obj.TrainingPlaceIsActive,
                name=obj.TrainingPlaceName,
                region_id=regions_dict[region_id] if region_id else None,
                created_at=make_dt_aware(obj.TrainingPlaceInsertDate),
                updated_at=make_dt_aware(obj.TrainingPlaceLastChangeDate),
            )

        self.out("success", f"✔ Hospitals migrated! ({Hospital.objects.count()} records)")
        """

        # ----------
        # Educations
        # ----------

        self.out("info", "Migrating educations...")

        for obj in session.query(Base.classes.Education).all():
            base = get_base_fields(obj, "Education")
            Education.objects.create(
                **base,
                id=obj.EducationID,
                name=obj.EducationName,
                faculty_id=obj.EducationFacultyID if obj.EducationFacultyID > 0 else None,
            )

        self.out("success", f"✔ Educations migrated! ({Education.objects.count()} records)")
