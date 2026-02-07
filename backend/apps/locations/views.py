from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Country, Region, City
from .serializers import (
    CountrySerializer,
    RegionSerializer,
    CitySerializer
)


class CountryListView(ListAPIView):
    queryset = Country.objects.all().order_by("name")
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]


class RegionListView(ListAPIView):
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Region.objects.filter(
            country_id=self.kwargs["country_id"]
        ).order_by("name")


class CityListView(ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return City.objects.filter(
            region_id=self.kwargs["region_id"]
        ).order_by("name")
