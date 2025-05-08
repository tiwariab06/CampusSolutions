# models.py

from django.db import models

class Resources(models.Model):
    Type = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    semester = models.IntegerField()
    Print = models.CharField(max_length=200)
    Price = models.IntegerField()
    Seller_email = models.EmailField()
    Seller_mobile = models.CharField(max_length=10)  # Use CharField for mobile
