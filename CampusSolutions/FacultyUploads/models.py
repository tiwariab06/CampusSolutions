from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Pyq(models.Model):
    class Semester(models.IntegerChoices):
        First = 1
        Second = 2
        Third = 3
        Fourth = 4
        Fifth = 5
        Sixth = 6
        Seventh = 7
        Eighth = 8

    url = models.FileField(upload_to="uploads/pyq")
    name = models.CharField(max_length=100)
    semester = models.IntegerField(choices=Semester.choices)
    session = models.CharField(max_length=100)


class Notes(models.Model):
    class Semester(models.IntegerChoices):
        First = 1
        Second = 2
        Third = 3
        Fourth = 4
        Fifth = 5
        Sixth = 6
        Seventh = 7
        Eight = 8

    type_choices = [("Printed", "Printed"), ("HandWritten", "HandWritten")]
    path = models.FileField(upload_to="uploads/Notes")
    sub_name = models.CharField(max_length=25)
    semester = models.IntegerField(choices=Semester.choices)
    type = models.CharField(max_length=25, choices=type_choices)
