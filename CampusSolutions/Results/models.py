from django.db import models


class Result(models.Model):
    class ExamTypeChoices(models.TextChoices):
        SESSIONAL_1 = "Sessional 1"
        SESSIONAL_2 = "Sessional 2"
        PUT = "Pre University Test (PUT)"

    Exam_Type = models.CharField(max_length=100, choices=ExamTypeChoices.choices)
    subject = models.CharField(max_length=200)
    max_marks = models.IntegerField()
    obtained_marks = models.IntegerField()
    student = models.ForeignKey(
        "Home.Students", on_delete=models.CASCADE
    )  # Assuming you have a Student model
