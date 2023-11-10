from django.db import models


class SpartaManager(models.Manager):
    """A manager for the models using the SPARTA database."""

    def get_queryset(self) -> models.QuerySet:
        """Return a queryset for the SPARTA database."""
        return super().get_queryset().using("sparta")


class SpartaModel(models.Model):
    """A model using the SPARTA database."""

    objects = SpartaManager()

    class Meta:  # noqa: D106
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """Raise an error when trying to save a SPARTA model."""
        raise ValueError("SPARTA database is not editable by Metis.")


class SpartaProject(SpartaModel):
    """A project from the SPARTA application."""

    id = models.IntegerField(primary_key=True, db_column="TrainingProjectID")
    name = models.CharField(max_length=255, db_column="TrainingProjectName")

    class Meta:  # noqa: D106
        db_table = "TrainingProject"
        managed = False

    def __str__(self) -> str:
        return self.name


class SpartaDiscipline(SpartaModel):
    """A discipline from the SPARTA application."""

    id = models.IntegerField(primary_key=True, db_column="TrainingDisciplineID")
    name = models.CharField(max_length=255, db_column="TrainingDisciplineName")

    class Meta:  # noqa: D106
        db_table = "TrainingDiscipline"
        managed = False

    def __str__(self) -> str:
        return self.name


class SpartaStudent(SpartaModel):
    """A student from the SPARTA application."""

    id = models.IntegerField(primary_key=True, db_column="TrainingStudentID")
    first_name = models.CharField(max_length=255, db_column="TrainingStudentFirstname")
    last_name = models.CharField(max_length=255, db_column="TrainingStudentLastname")
    email = models.CharField(max_length=255, db_column="TrainingStudentEMail")
    number = models.CharField(max_length=255, db_column="TrainingStudentCode")
    project = models.ForeignKey(
        SpartaProject,
        on_delete=models.DO_NOTHING,
        db_column="TrainingStudentTrainingProjectID",
        related_name="students",
    )

    class Meta:  # noqa: D106
        db_table = "TrainingStudent"
        managed = False

    def __str__(self) -> str:
        return f"{self.name} ({self.number})"

    @property
    def name(self) -> str:
        """Return the full name of the student."""
        return f"{self.first_name} {self.last_name}"


class SpartaInternship(SpartaModel):
    """An internship from the SPARTA application."""

    id = models.IntegerField(primary_key=True, db_column="TrainingID")
    project = models.ForeignKey(
        SpartaProject,
        on_delete=models.DO_NOTHING,
        db_column="TrainingTrainingProjectID",
        related_name="internships",
    )
    student = models.ForeignKey(
        SpartaStudent,
        on_delete=models.DO_NOTHING,
        db_column="TrainingTrainingStudentID",
        related_name="internships",
    )
    discipline = models.ForeignKey(
        SpartaDiscipline,
        on_delete=models.DO_NOTHING,
        db_column="TrainingTrainingDisciplineID",
        related_name="internships",
    )
    start_date = models.DateField(db_column="TrainingStartDate")
    end_date = models.DateField(db_column="TrainingEndDate")
    updated_at = models.DateTimeField(db_column="TrainingLastChangeDate")
    is_active = models.BooleanField(db_column="TrainingIsActive")

    class Meta:  # noqa: D106
        db_table = "Training"
        managed = False
