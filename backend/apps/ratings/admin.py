from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "reviewer",
        "rated_user",
        "rating",
        "short_review",
        "created_at",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    search_fields = (
        "reviewer__username",
        "rated_user__username",
        "review",
    )

    ordering = ("-created_at",)

    list_per_page = 20
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("reviewer", "rated_user")

    def short_review(self, obj):
        return obj.review[:50] + "..." if len(obj.review) > 50 else obj.review

    short_review.short_description = "Review"
    
    def colored_rating(self, obj):
        color = "green" if obj.rating >= 4 else "orange" if obj.rating == 3 else "red"
        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            obj.rating
        )

    colored_rating.short_description = "Rating"
