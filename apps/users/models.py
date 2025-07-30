from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django_countries.fields import CountryField

class User(AbstractUser):
    email = models.EmailField(unique=True)
    google_id = models.CharField(unique=True, blank=True, null=True, max_length=255)

    def __str__(self):
        return self.username
    
class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    address = models.CharField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.address

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    phone = models.CharField(16, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)

def default_expiry_time():
    return timezone.now() + timedelta(seconds=35)

class Code(models.Model):
    code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry_time)

    def is_expired(self):
        return timezone.now() > self.expires_at