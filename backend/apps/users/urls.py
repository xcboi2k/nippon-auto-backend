from django.urls import path
from .views import (
    HealthCheckView,
    
    EmailTokenObtainPairView,
    ProfileView,
    UploadProfilePictureView,
    DeleteProfilePictureView,
    SignupView
)

urlpatterns = [
    # path("health/", HealthCheckView.as_view(), name="health-check"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
    path("profile-picture/upload/", UploadProfilePictureView.as_view()),
    path("profile-picture/delete/", DeleteProfilePictureView.as_view()),
    # path("auth/login/", EmailTokenObtainPairView.as_view(), name="token_login"),
    # path("auth/signup/", SignupView.as_view(), name="signup"),
]
