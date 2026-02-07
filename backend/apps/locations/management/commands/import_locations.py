import json
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.locations.models import Country, Region, City

@transaction.atomic
class Command(BaseCommand):
    help = "Import countries, regions, cities"

    def handle(self, *args, **kwargs):

        with open("data/world.json", encoding="utf-8") as f:
            data = json.load(f)
            print('world.json has been loaded')

        for c in data:

            country, _ = Country.objects.get_or_create(
                name=c["name"],
                code=c["iso2"],
                defaults={
                    "phone_code": "+" + c["phonecode"]
                }
            )
            print(f'{country.name} has been imported')

            for s in c["states"]:

                region, _ = Region.objects.get_or_create(
                    country=country,
                    name=s["name"]
                )
                print(f'{region.name} has been imported')

                for city in s["cities"]:

                    City.objects.get_or_create(
                        region=region,
                        name=city["name"]
                    )
                    print(f'{city.name} has been imported')

        self.stdout.write(self.style.SUCCESS("World data imported"))
