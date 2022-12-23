from django.utils import timezone

from sparta.models.users import User
from .base import DataMigration


class UserDataMigration(DataMigration):
    migrate_base_fields = False
    legacy_table = "FWAccount"
    model = User

    def get_fields(self, row) -> dict:
        return {
            "id": row.FWAccountID,
            "is_active": row.FWAccountIsActive == 1,
            "username": f"{row.FWAccountName.replace(' ', '')}{row.FWAccountID}",
            "email": row.FWAccountUGentCASID.lower() if row.FWAccountUGentCASID else "",
            "password": row.FWAccountPasswordHash or "",
            "last_login": self.aware(row.FWAccountLastLogin) if row.FWAccountLastLogin else None,
            "date_joined": self.aware(row.FWAccountInsertDate) if row.FWAccountInsertDate else timezone.now(),
        }
