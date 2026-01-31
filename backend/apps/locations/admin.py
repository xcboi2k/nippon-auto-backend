from django.contrib import admin
from .models import MyCountry, MyRegion, MyCity

@admin.register(MyCountry)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso2_code', 'iso3_code')  # use helper methods
    search_fields = ('name',)
    ordering = ('name',)

    # Methods to display ISO codes
    def iso2_code(self, obj):
        return getattr(obj, 'iso2', '')  # safe access
    iso2_code.short_description = "ISO2"

    def iso3_code(self, obj):
        return getattr(obj, 'iso3', '')  # safe access
    iso3_code.short_description = "ISO3"


@admin.register(MyRegion)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'slug')
    search_fields = ('name', 'slug', 'country__name')
    list_filter = ('country',)
    ordering = ('country', 'name')


@admin.register(MyCity)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'country', 'slug')
    search_fields = ('name', 'slug', 'region__name', 'country__name')
    list_filter = ('country', 'region')
    ordering = ('country', 'region', 'name')
