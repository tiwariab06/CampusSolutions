from django.db import models

# Create your models here.
class Submitted_Assignments(models.Model):
    class Semester(models.IntegerChoices):
        First = 1
        Second = 2
        Third = 3
        Fourth = 4
        Fifth = 5
        Sixth = 6
        Seventh = 7
        Eight = 8
    subject = models.CharField(max_length=50)
    assignment_number = models.IntegerField()
    path = models.FileField(upload_to="uploads/Submitted_Assignments")
    semester = models.IntegerField(choices=Semester.choices)
    section = models.CharField(max_length=10)
    description = models.TextField()
    submission_deadline = models.DateField()
    submitted_on=models.DateField()
