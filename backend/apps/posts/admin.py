from django.contrib import admin
from django.utils.html import format_html

from .models import Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return "No Image"

    preview.short_description = "Preview"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "created_at")
    search_fields = ("content", "user__username")
    list_filter = ("created_at",)
    inlines = [PostImageInline]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "preview")

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" />',
                obj.image.url
            )
        return "-"

    preview.short_description = "Image"
