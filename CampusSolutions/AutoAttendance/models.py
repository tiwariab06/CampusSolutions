from django.db import models
from Home.models import*
# Create your models here.
# models.py

class RegisteredFace(models.Model):
    user = models.OneToOneField(Students, on_delete=models.CASCADE)  # Link to Django user
    student_id = models.IntegerField()  # From your existing Student model
    roll_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    face_image = models.ImageField(upload_to='registered_faces/')
    is_registered = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"
