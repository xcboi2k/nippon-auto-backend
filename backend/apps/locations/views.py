from rest_framework import generics
from .models import MyCountry, MyRegion, MyCity
from .serializers import CountrySerializer, RegionSerializer, CitySerializer

# -----------------------------
# Countries API
# -----------------------------
class CountryListAPIView(generics.ListAPIView):
    queryset = MyCountry.objects.all().order_by('name')
    serializer_class = CountrySerializer


# -----------------------------
# Regions API
# -----------------------------
class RegionListAPIView(generics.ListAPIView):
    serializer_class = RegionSerializer

    def get_queryset(self):
        queryset = MyRegion.objects.select_related('country').all().order_by('country__name', 'name')
        return queryset


# -----------------------------
# Cities API (distinct)
# -----------------------------
class CityListAPIView(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        # Use values + distinct for DB-level duplicate removal
        queryset = MyCity.objects.select_related('region', 'country').all().order_by('country__name', 'region__name', 'name')
        return queryset

class CountryPhoneCodeView(generics.ListAPIView):

    def get(self, request):

        data = []

        for code, name in list(countries):

            data.append({
                "code": code,
                "name": name,
                "dial_code": countries.by_code(code).calling_codes[0]
                if countries.by_code(code).calling_codes
                else None
            })

        return Response(data)