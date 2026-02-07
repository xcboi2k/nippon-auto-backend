from django.contrib import admin
from .models import Country, Region, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "phone_code")
    search_fields = ("name", "code")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")
    list_filter = ("country",)
    search_fields = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region")
    list_filter = ("region__country", "region")
    search_fields = ("name",)
