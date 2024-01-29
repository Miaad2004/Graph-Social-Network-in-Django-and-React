from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    date_of_birth = models.DateField()
    university_location = models.CharField(max_length=100, blank=True)
    field = models.CharField(max_length=100, blank=True)
    workplace = models.CharField(max_length=100, blank=True)
    specialties = models.JSONField(default=list, null=True, blank=True)
    
    def __str__(self):
        return self.username

class Connection(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='user2', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1} - {self.user2} ({self.creation_date})"

