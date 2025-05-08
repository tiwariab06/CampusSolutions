from django.db import models
from django.utils import timezone


# Create your models here.
class Faculty_Messages(models.Model):
    faculty_id = models.IntegerField()
    sent_to_student_id = models.IntegerField()
    content = models.TextField()
    sent_at = models.DateTimeField()


class Student_Messages(models.Model):
    student_id = models.IntegerField()
    sent_to_faculty_id = models.IntegerField()
    content = models.TextField()
    sent_at = models.DateTimeField()
