from django.db.models import Avg
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Rating
from .serializers import RatingSerializer


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Rating.objects.select_related(
            "reviewer",
            "rated_user"
        ).order_by("-created_at")

    def update_user_rating_stats(self, user):
        from apps.accounts.models import Profile  # adjust path if needed

        stats = Rating.objects.filter(
            rated_user=user
        ).aggregate(
            avg_rating=Avg("rating")
        )

        profile = user.profile
        profile.average_rating = round(
            stats["avg_rating"] or 0, 2
        )
        profile.total_ratings = Rating.objects.filter(
            rated_user=user
        ).count()

        profile.save()

    def perform_create(self, serializer):
        rating = serializer.save(
            reviewer=self.request.user
        )
        self.update_user_rating_stats(
            rating.rated_user
        )

    def perform_update(self, serializer):
        rating = serializer.save()
        self.update_user_rating_stats(
            rating.rated_user
        )

    def perform_destroy(self, instance):
        rated_user = instance.rated_user
        instance.delete()
        self.update_user_rating_stats(
            rated_user
        )
