from sparta.models.stages.projects import Project, Period
from .base import DataMigration


class ProjectDataMigration(DataMigration):
    legacy_table = "TrainingProject"
    model = Project

    def get_fields(self, row) -> dict:
        return {
            "id": row.TrainingProjectID,
            "name": row.TrainingProjectName,
            "is_visible_to_students": row.TrainingProjectIsVisibleForStudent == 1,
            "is_visible_to_contacts": row.TrainingProjectIsVisibleForContact == 1,
        }


class PeriodDataMigration(DataMigration):
    legacy_table = "TrainingPeriod"
    model = Period

    def get_fields(self, row) -> dict:
        return {
            "id": row.TrainingPeriodID,
            "name": row.TrainingPeriodName,
            "project_id": row.TrainingPeriodTrainingProjectID,
            "start_date": row.TrainingPeriodStartDate,
            "end_date": row.TrainingPeriodEndDate,
        }
