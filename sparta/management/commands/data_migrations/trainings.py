from sparta.models.users import User
from sparta.models.stages.trainings import Training
from .base import DataMigration


class TrainingDataMigration(DataMigration):
    legacy_table = "Training"
    model = Training
    user_ids = {}

    def get_fields(self, row) -> dict:
        if not self.user_ids:
            self.user_ids = set(User.objects.values_list("id", flat=True))

        return {
            "id": row.TrainingID,
            "period_id": row.TrainingTrainingPeriodID if row.TrainingTrainingPeriodID else None,
            "student_id": row.TrainingTrainingStudentID if row.TrainingTrainingStudentID in self.user_ids else None,
            "place_id": row.TrainingTrainingPlaceID if row.TrainingTrainingPlaceID else None,
        }
