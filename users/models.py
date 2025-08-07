from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

PRIVACY_CHOICES = [
    ('public', 'Public'),
    ('friends', 'Friends'),
    ('private', 'Private'),
]

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    email_notifications = models.BooleanField(default=True)
    profile_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} Settings"
