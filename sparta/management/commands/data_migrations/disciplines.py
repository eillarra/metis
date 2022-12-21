from .base import DataMigration

from sparta.models.disciplines import Discipline


class DisciplineDataMigration(DataMigration):
    legacy_table = "TrainingDiscipline"
    model = Discipline

    def migrate():
        """
        for obj in session.query(Base.classes.TrainingDiscipline).all():
            base = get_base_fields(obj, "TrainingDiscipline")
            Discipline.objects.create(
                **base,
                id=obj.TrainingDisciplineID,
                name=obj.TrainingDisciplineName,
            )

        self.out("success", f"✔ Disciplines migrated! ({Discipline.objects.count()} records)")
        """
        pass
