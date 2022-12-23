from django.core.management.base import BaseCommand
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy import create_engine

from .data_migrations.absences import AbsenceDataMigration
from .data_migrations.disciplines import DisciplineDataMigration
from .data_migrations.faculties import FacultyDataMigration, DegreeDataMigration
from .data_migrations.places import PlaceDataMigration
from .data_migrations.projects import ProjectDataMigration, PeriodDataMigration
from .data_migrations.trainings import TrainingDataMigration
from .data_migrations.users import UserDataMigration


def automap_tables(uri) -> tuple:
    """http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html"""
    Base = automap_base()
    engine = create_engine(uri)
    Base.prepare(engine, reflect=True)

    return Base, OrmSession(engine)


class Command(BaseCommand):
    help = "Migrates legacy SPARTA database to new tables."

    def handle(self, *args, **options):
        print("Mapping legacy database...")
        automap = automap_tables("mysql://root:password@127.0.0.1:3306/sparta_old")

        # UserDataMigration(automap).migrate()  # this should be the first one
        FacultyDataMigration(automap).migrate()
        DegreeDataMigration(automap).migrate()
        DisciplineDataMigration(automap).migrate()
        ProjectDataMigration(automap).migrate()
        PeriodDataMigration(automap).migrate()
        PlaceDataMigration(automap, is_final=False).migrate()
        TrainingDataMigration(automap).migrate()
        AbsenceDataMigration(automap).migrate()
