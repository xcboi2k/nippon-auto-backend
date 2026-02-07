from django.urls import path
from .views import CountryListView, RegionListView, CityListView

urlpatterns = [
    path("countries/", CountryListView.as_view()),

    path(
        "countries/<int:country_id>/regions/",
        RegionListView.as_view()
    ),

    path(
        "regions/<int:region_id>/cities/",
        CityListView.as_view()
    ),
]
