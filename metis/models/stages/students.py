from django.db import models

from ..base import BaseModel


class Student(BaseModel):
    """
    A Student is a User that is linked to a Project.
    TODO: This model is used to register students' preferences too.
    """

    user = models.ForeignKey("metis.User", related_name="student_records", on_delete=models.CASCADE)
    project = models.ForeignKey("metis.Project", related_name="students", on_delete=models.CASCADE)
    block = models.ForeignKey("metis.ProgramBlock", related_name="students", on_delete=models.CASCADE)
    track = models.ForeignKey("metis.Track", related_name="students", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["project", "block__position"]
