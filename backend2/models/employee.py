from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings

class Employee(models.Model):
    def upload_to(instance, filename):
        return f'employee_pictures/{instance.full_name}_{filename}'

    id = models.BigAutoField(primary_key=True)  # Ensure this remains the primary key
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20)
    picture = models.ImageField(upload_to=upload_to, null=True, blank=True)
    
    @property
    def picture_url(self):
        if self.picture:
            return f"{settings.MEDIA_URL}{self.picture}"
        return None

    def __str__(self):
        return self.full_name