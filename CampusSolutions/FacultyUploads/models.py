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
    sub_name = models.TextField()
    semester = models.IntegerField(choices=Semester.choices)
    type = models.CharField(max_length=25, choices=type_choices)


class Assignments(models.Model):
    class Semester(models.IntegerChoices):
        First = 1
        Second = 2
        Third = 3
        Fourth = 4
        Fifth = 5
        Sixth = 6
        Seventh = 7
        Eight = 8

    choices = [
        ("Computer Science and Engineering", "Computer Science and Engineering"),
        (
            "Electrical and Electronics Engineering",
            "Electrical and Electronics Engineering",
        ),
        (
            "Electronics and Communication Engineering",
            "Electronics and Communication Engineering",
        ),
        (
            "Mechanical Engineering",
            "Mechanical Engineering",
        ),
    ]
    subject = models.CharField(max_length=50)
    assignment_number = models.IntegerField()
    path = models.FileField(upload_to="uploads/Assignments")
    semester = models.IntegerField(choices=Semester.choices)
    department = models.CharField(max_length=50, choices=choices)
    section = models.CharField(max_length=10)
    description = models.TextField()
    submission_deadline = models.DateField()
