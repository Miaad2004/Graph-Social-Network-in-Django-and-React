from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    birthday = models.DateField()
    university = models.CharField(max_length=100, blank=False)
    field = models.CharField(max_length=100, blank=False)
    workplace = models.CharField(max_length=100, blank=True)
    specialties = models.JSONField(default=list, blank=True)
    profile_photo = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    def get_shared_specialties_count(self, other_user):
        count = 0
        for specialty in self.specialties:
            if specialty in other_user.specialties:
                count += 1
        return count
    
    def get_correlation_score(self, other_user):
        shared_specialties_count = self.get_shared_specialties_count(other_user)
        have_shared_field = self.field == other_user.field
        have_shared_university = self.university == other_user.university
        have_shared_workplace = self.workplace == other_user.workplace
        age_difference = abs(self.birthday.year - other_user.birthday.year)
        
        if age_difference == 0:
            age_difference_score = 0  
        else:
            age_difference_score = 1 / age_difference

        return 2 * shared_specialties_count + 2 * have_shared_field + \
               have_shared_university + have_shared_workplace + age_difference_score
    
    


class Connection(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='user2', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1} - {self.user2} ({self.creation_date})"

