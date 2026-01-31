from rest_framework import serializers
from .models import MyCountry, MyRegion, MyCity

# -----------------------------
# Country Serializer
# -----------------------------
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCountry
        fields = ('id', 'name')


# -----------------------------
# Region Serializer
# -----------------------------
class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = MyRegion
        fields = ('id', 'name', 'country')


# -----------------------------
# City Serializer
# -----------------------------
class CitySerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name', read_only=True)
    region = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = MyCity
        fields = ('id', 'name', 'region', 'country')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Combine unique key for filtering duplicates
        key = f"{rep['name']}-{rep['region']}-{rep['country']}"
        if not hasattr(self, '_seen'):
            self._seen = set()
        if key in self._seen:
            return None
        self._seen.add(key)
        return rep
