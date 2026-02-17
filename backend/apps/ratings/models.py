from django.db import models
from django.conf import settings
from apps.listings.models import Listing


class Rating(models.Model):
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_ratings"
    )

    rated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_ratings"
    )

    rating = models.PositiveSmallIntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "rated_user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reviewer.username} → {self.rated_user.username} ({self.rating})"

