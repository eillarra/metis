from sparta.models.rel.remarks import Remark
from sparta.models.stages.absences import Absence
from sparta.models.stages.trainings import Training
from .base import DataMigration


class AbsenceDataMigration(DataMigration):
    legacy_table = "TrainingAbsence"
    model = Absence

    def get_fields(self, row) -> dict:
        """
        try:
            training_id = (
                Training.objects.filter(
                    student_id=row.TrainingAbsenceTrainingStudentID,
                    period__project_id=row.TrainingAbsenceTrainingProjectID,
                    period__start_date__lte=row.TrainingAbsenceStartDate,
                    period__end_date__gte=row.TrainingAbsenceEndDate,
                )
                .first()
                .id
            )
        except AttributeError:
            training_id = None
        """

        training_id = None

        return {
            "id": row.TrainingAbsenceID,
            "status": {
                1: Absence.ACCEPTED,
                2: Absence.PENDING,
                3: Absence.REJECTED,
            }[row.TrainingAbsenceTrainingAbsenceStatusID] if row.TrainingAbsenceTrainingAbsenceStatusID < 4 else Absence.PENDING,
            "training_id": training_id,
            "start_at": self.aware(row.TrainingAbsenceStartDate) if row.TrainingAbsenceStartDate else None,
            "end_at": self.aware(row.TrainingAbsenceEndDate) if row.TrainingAbsenceEndDate else self.aware(row.TrainingAbsenceStartDate),
        }

    def post_save(self) -> None:
        print("Adding remarks by 'stage bureau'...")

        for row in self.get_legacy_data():
            if row.TrainingAbsenceRemarkByBureau:
                obj = Absence.objects.get(id=row.TrainingAbsenceID)
                Remark.objects.create(
                    content_object=obj,
                    text=row.TrainingAbsenceRemarkByBureau,
                    created_by=None,
                    created_at=self.aware(row.TrainingAbsenceLastChangeDate),
                    updated_at=self.aware(row.TrainingAbsenceLastChangeDate),
                )
