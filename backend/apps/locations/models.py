from django.db import models
from cities_light.models import Country, Region, City

# -----------------------------
# Proxy models for admin
# -----------------------------
class MyCountry(Country):
    class Meta:
        proxy = True
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class MyRegion(Region):
    class Meta:
        proxy = True
        verbose_name = "Region / State"
        verbose_name_plural = "Regions / States"

class MyCity(City):
    class Meta:
        proxy = True
        verbose_name = "City"
        verbose_name_plural = "Cities"
