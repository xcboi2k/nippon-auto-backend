from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_delete, sender=Profile)


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
def delete_profile_picture(sender, instance, **kwargs):
    if instance.profilePicture:
        instance.profilePicture.delete(save=False)