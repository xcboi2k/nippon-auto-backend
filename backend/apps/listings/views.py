from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Listing
from .serializers import ListingSerializer
from .pagination import ListingPagination


class ListingViewSet(ModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ListingPagination

    def get_queryset(self):
        return Listing.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
