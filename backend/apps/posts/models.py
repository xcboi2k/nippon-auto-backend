from django.db import models
from django.conf import settings

from cloudinary.models import CloudinaryField

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.content[:30]}"


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="images",
        on_delete=models.CASCADE
    )
    # image = models.ImageField(upload_to="posts/")
    image = CloudinaryField(
        "post_image",
        folder="posts",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Image for post {self.post.id}"
