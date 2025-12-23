from django.urls import path
from .views import (
    HealthCheckView,
    ProfileView,
    EmailTokenObtainPairView
)

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("users/me/", ProfileView.as_view(), name="user-profile"),
    path("auth/login/", EmailTokenObtainPairView.as_view(), name="token_login"),
]
