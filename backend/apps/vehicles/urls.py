from django.urls import path
from .views import VehicleOptionsView

urlpatterns = [
    path("options/", VehicleOptionsView.as_view(), name="vehicle-options"),
]
