import pytz

from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils.timezone import make_aware
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy import create_engine
from typing import Optional


def automap_tables(self, uri):
    """http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html"""
    Base = automap_base()
    engine = create_engine(uri)
    Base.prepare(engine, reflect=True)

    return Base, OrmSession(engine)


class DataMigration:
    User = get_user_model()

    def __init__(self) -> None:
        self._base, self._session = automap_tables("mysql://root@127.0.0.1:3306/sparta_old")
        self._models = self._base.classes
