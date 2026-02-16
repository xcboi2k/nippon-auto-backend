from django.db import models
from django.conf import settings

from cloudinary.models import CloudinaryField

class Listing(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings"
    )

    vehicle_type = models.CharField(max_length=50)
    engine_type = models.CharField(max_length=50)
    drivetrain = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)

    vehicle_model = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    year = models.PositiveIntegerField()
    kilometers = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_model} - {self.price}"


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = CloudinaryField(
        "listing_image",
        folder="listings",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Image for listing {self.listing.id}"
