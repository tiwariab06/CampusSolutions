from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Pyq(models.Model):
    url = models.FileField(upload_to="uploads/pyq")
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
