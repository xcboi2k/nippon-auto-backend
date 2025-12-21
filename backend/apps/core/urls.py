# backend/apps/users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Example route
    path("", views.health_check, name="health-check"),
]

