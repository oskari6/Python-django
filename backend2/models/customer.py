from django.db import models
from django.contrib.auth.models import User
        
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
#from django.contrib.auth.models import AbstractUser   

# making custom User adds more complexity not needed right now
# class User(AbstractUser):
#     email = models.EmailField(max_length=255, unique=True)
#     name = models.CharField(max_length=255, blank=True, null=True)

#     REQUIRED_FIELDS = ['name']

#     def __str__(self):
#         return self.email