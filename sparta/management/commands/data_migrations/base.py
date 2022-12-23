import requests
import sys

from colorama import Fore, Style
from datetime import datetime
from contextlib import contextmanager
from django.utils.timezone import make_aware
from typing import Optional
from zoneinfo import ZoneInfo

from sparta.models.rel.links import Link


@contextmanager
def suppress_autotime(model, field_names):
    """
    From https://stackoverflow.com/a/59898220/519995
    idea taken here https://stackoverflow.com/a/35943149/1731460
    """
    fields_state = {}

    for field_name in field_names:
        field = model._meta.get_field(field_name)
        fields_state[field] = {"auto_now": field.auto_now, "auto_now_add": field.auto_now_add}

    for field in fields_state:
        field.auto_now = False
        field.auto_now_add = False

    try:
        yield
    finally:
        for field, state in fields_state.items():
            field.auto_now = state["auto_now"]
            field.auto_now_add = state["auto_now_add"]


class DataMigration:
    migrate_base_fields = True
    TZ = ZoneInfo("Europe/Brussels")
    legacy_table: str
    model = None

    def __init__(self, automap: tuple, *, is_final: bool = True) -> None:
        self._base, self._session = automap
        self._models = self._base.classes
        self.stdout = sys.stdout
        self.is_final = is_final

    def aware(self, naive: datetime) -> Optional[datetime]:
        return make_aware(naive, timezone=self.TZ)

    def get_legacy_data(self):
        return self._session.query(self._models[self.legacy_table]).all()

    def get_base_fields(self, row, prefix: str) -> dict:
        try:
            created_at = self.aware(getattr(row, f"{prefix}InsertDate"))
        except AttributeError:
            created_at = self.aware(getattr(row, f"{prefix}LastChangeDate"))

        created_by = getattr(row, f"{prefix}InsertAccountID")
        updated_by = getattr(row, f"{prefix}LastChangeAccountID") or 32
        position = getattr(row, f"{prefix}OrderNumber")

        return {
            "is_active": getattr(row, f"{prefix}IsActive"),
            "position": position if position <= 32767 else 32767,
            "created_at": created_at,
            "created_by_id": created_by if created_by else updated_by,
            "updated_at": self.aware(getattr(row, f"{prefix}LastChangeDate")),
            "updated_by_id": updated_by,
        }

    def get_fields(self, row) -> dict:
        return {}

    def post_save(self) -> None:
        pass

    def migrate(self):
        print(f"Migrating {self.legacy_table}...")

        with suppress_autotime(self.model, ["created_at", "updated_at"] if self.migrate_base_fields else []):
            for row in self.get_legacy_data():
                self.model.objects.create(
                    **self.get_base_fields(row, self.legacy_table) if self.migrate_base_fields else {},
                    **self.get_fields(row),
                )

        self.post_save()

        print(
            f"{Fore.GREEN}"
            f"✔ Migrated {self.model.objects.count()} records to {self.model._meta.label}! "
            f"{Style.RESET_ALL}"
        )

    def add_link(self, obj, url, type: str = Link.WEBSITE):
        if self.is_final:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    Link.objects.create(
                        content_object=obj,
                        type=type,
                        url=url,
                    )
            except requests.exceptions.ConnectionError:
                pass
