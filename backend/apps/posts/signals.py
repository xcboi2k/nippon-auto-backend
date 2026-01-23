from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import PostImage

@receiver(post_delete, sender=PostImage)
def delete_post_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
