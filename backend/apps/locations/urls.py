from django.urls import path
from .views import *


urlpatterns = [

    path("countries/", CountryListAPIView.as_view()),

    path(
        "countries/<int:country_id>/regions/",
        RegionListAPIView.as_view()
    ),

    path(
        "regions/<int:region_id>/cities/",
        CityListAPIView.as_view()
    ),
    path("phone-codes/", CountryPhoneCodeView.as_view()),
]
