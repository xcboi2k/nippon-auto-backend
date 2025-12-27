from django.contrib.auth.models import User
from django.db import models

from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    # duplicated basic identity fields
    firstName = models.CharField(max_length=150)
    lastName = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()

    # business / extra fields
    shopName = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    mobileNumber = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profilePicture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username


def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    if self.profilePicture:
        img = Image.open(self.profilePicture.path)

        MAX_SIZE = (300, 300)
        img.thumbnail(MAX_SIZE)

        img.save(self.profilePicture.path)