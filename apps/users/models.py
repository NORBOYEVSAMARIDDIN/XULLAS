from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

def default_expiry_time():
    return timezone.now() + timedelta(seconds=35)

class Code(models.Model):
    code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry_time)

    def is_expired(self):
        return timezone.now() > self.expires_at
