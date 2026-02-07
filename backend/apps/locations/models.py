from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)   # PH, US
    phone_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Region(models.Model):
    country = models.ForeignKey(
        Country,
        related_name="regions",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.country.code}"


class City(models.Model):
    region = models.ForeignKey(
        Region,
        related_name="cities",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.region.name}"
