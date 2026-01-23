from django.contrib import admin
from django.utils.html import format_html
from .models import Post, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    max_num = 3
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 80px; border-radius: 6px;" />',
                obj.image.url,
            )
        return "No image"

    preview.short_description = "Preview"
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "short_content", "created_at")
    search_fields = ("content", "user__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    def short_content(self, obj):
        return obj.content[:40] + "..." if len(obj.content) > 40 else obj.content
    
    def has_module_permission(self, request):
        return request.user.is_superuser
    
    def image_count(self, obj):
        return obj.images.count()
