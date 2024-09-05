from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class CapturedPhoto(models.Model):
    photo = models.ImageField(upload_to='images/')
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Photo {self.id} by {self.user} on {self.date}"
    


class SaveImage(models.Model):
    # location=models.CharField(max_length=50)
    # latitude=models.CharField(max_length=50)
    # longitude=models.CharField(max_length=50)
    image=models.ImageField(upload_to='images/')