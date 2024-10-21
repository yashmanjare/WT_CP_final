from django.db import models

class UserProfile(models.Model):
    mobile = models.CharField(max_length=15, primary_key=True)  
    name = models.CharField(max_length=100)  
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128) 

    def __str__(self):
        return self.name  

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
