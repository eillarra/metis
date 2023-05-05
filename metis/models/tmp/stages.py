from django.db import models


class TmpPlaceData(models.Model):
    place = models.ForeignKey("metis.Place", on_delete=models.CASCADE)
    discipline = models.ForeignKey("metis.Discipline", on_delete=models.CASCADE)
    remarks = models.TextField(null=True, blank=True)


class TmpStudent(models.Model):
    project = models.ForeignKey("metis.Project", on_delete=models.CASCADE)
    block = models.ForeignKey("metis.ProgramBlock", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    period = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TmpMentor(models.Model):
    project = models.ForeignKey("metis.Project", on_delete=models.CASCADE)
    place = models.ForeignKey("metis.Place", null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_numbers = models.JSONField(null=True, blank=True)
    emails = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class TmpInternship(models.Model):
    project = models.ForeignKey("metis.Project", on_delete=models.CASCADE)
    place = models.ForeignKey("metis.Place", on_delete=models.CASCADE)
    student = models.ForeignKey(TmpStudent, null=True, blank=True, on_delete=models.SET_NULL)
    mentors = models.ManyToManyField(TmpMentor)
    remarks = models.TextField()

    project_name = models.CharField(max_length=255)
    block_name = models.CharField(max_length=255)
    period = models.CharField(max_length=255)

    def __str__(self):
        return self.student
