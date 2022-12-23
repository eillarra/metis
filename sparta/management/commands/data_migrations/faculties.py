from sparta.models.faculties import Faculty, Degree
from .base import DataMigration


class FacultyDataMigration(DataMigration):
    legacy_table = "Faculty"
    model = Faculty

    def get_fields(self, row) -> dict:
        return {
            "id": row.FacultyID,
            "name": row.FacultyName,
        }


class DegreeDataMigration(DataMigration):
    legacy_table = "Education"
    model = Degree

    def get_fields(self, row) -> dict:
        return {
            "id": row.EducationID,
            "name": row.EducationName,
            "faculty_id": row.EducationFacultyID if row.EducationFacultyID else None,
        }
