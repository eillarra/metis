from sparta.models.disciplines import Discipline
from .base import DataMigration

class DisciplineDataMigration(DataMigration):
    legacy_table = "TrainingDiscipline"
    model = Discipline

    def get_fields(self, row) -> dict:
        return {
            "id": row.TrainingDisciplineID,
            "name": row.TrainingDisciplineName,
        }
