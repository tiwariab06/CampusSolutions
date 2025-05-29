from django.db import models
from django.utils import timezone


# Create your models here.
class Faculty_Messages(models.Model):
    faculty_id = models.IntegerField()
    sent_to_student_id = models.IntegerField()
    content = models.TextField()
    sent_at = models.DateTimeField()
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('read', 'Read')], default='sent')


class Student_Messages(models.Model):
    student_id = models.IntegerField()
    sent_to_faculty_id = models.IntegerField()
    content = models.TextField()
    sent_at = models.DateTimeField()
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('read', 'Read')], default='sent')
