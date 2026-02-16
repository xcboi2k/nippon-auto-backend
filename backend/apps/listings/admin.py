from django.contrib import admin
from django.utils.html import format_html
from .models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 0
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover;" />',
                obj.image.url
            )
        return "-"
    
    image_preview.short_description = "Preview"

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "vehicle_model",
        "vehicle_type",
        "price",
        "year",
        "kilometers",
        "image_count",
        "user",
        "created_at",
    )

    list_filter = (
        "vehicle_type",
        "engine_type",
        "drivetrain",
        "transmission",
        "year",
        "created_at",
    )

    search_fields = (
        "vehicle_model",
        "user__username",
    )

    ordering = ("-created_at",)

    list_per_page = 20

    readonly_fields = ("created_at",)

    inlines = [ListingImageInline]
    
    def image_count(self, obj):
        return obj.images.count()

    image_count.short_description = "Images"
