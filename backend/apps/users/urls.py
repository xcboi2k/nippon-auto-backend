from django.urls import path
from .views import (
    HealthCheckView,
    
    EmailTokenObtainPairView,
    ProfileView,
    DeleteProfilePictureView,
    SignupView
)

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("users/me/", ProfileView.as_view(), name="user-profile"),
    path("users/me/profile-picture/", DeleteProfilePictureView.as_view()),
    path("auth/login/", EmailTokenObtainPairView.as_view(), name="token_login"),
    path("auth/signup/", SignupView.as_view(), name="signup"),
]
