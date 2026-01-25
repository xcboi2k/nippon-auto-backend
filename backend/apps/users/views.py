import logging

from django.conf import settings
from django.http import JsonResponse

from drf_spectacular.utils import extend_schema, OpenApiExample

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import EmailTokenObtainPairSerializer, SignupSerializer
from .r2 import generate_presigned_url


logger = logging.getLogger(__name__)


# ---------------------------
# Health check
# ---------------------------

class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()


@extend_schema(responses=HealthCheckSerializer)
class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logger.info("Health check requested")
        return Response({"status": "ok"})


# ---------------------------
# Profile endpoint
# ---------------------------

class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        user = self.request.user
        logger.debug(f"Fetching profile for user {user.id}")
        return user.profile

    def update(self, request, *args, **kwargs):
        logger.info(f"Profile update requested by user {request.user.id}")
        return super().update(request, *args, **kwargs)


# ---------------------------
# JWT login using email
# ---------------------------

@extend_schema(
    request=EmailTokenObtainPairSerializer,
    examples=[
        OpenApiExample(
            "Sample Login",
            summary="Email/password input",
            value={"email": "user@example.com", "password": "password123"},
            request_only=True,
        )
    ],
    responses={200: EmailTokenObtainPairSerializer},
)
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        logger.info(f"Login attempt: {request.data.get('email')}")
        return super().post(request, *args, **kwargs)


# ---------------------------
# Sign Up
# ---------------------------

@extend_schema(
    request=SignupSerializer,
    responses={201: None},
    examples=[
        OpenApiExample(
            "Signup Example",
            value={
                "firstName": "John",
                "lastName": "Doe",
                "userName": "johndoe",
                "email": "john@example.com",
                "password": "password123",
                "confirmPassword": "password123",
            },
            request_only=True,
        )
    ],
)
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")

        logger.info(f"Signup attempt: {email}")

        serializer = SignupSerializer(data=request.data)

        if not serializer.is_valid():
            # Get first error message
            first_error = next(iter(serializer.errors.values()))[0]

            return Response(
                {
                    "success": False,
                    "message": str(first_error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Account created successfully"
            },
            status=status.HTTP_201_CREATED
        )


# ---------------------------
# Delete Profile Picture
# ---------------------------

class DeleteProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):

        profile = request.user.profile
        user_id = request.user.id

        if profile.profilePicture:
            logger.info(f"Deleting profile picture for user {user_id}")

            profile.profilePicture.delete(save=False)
            profile.profilePicture = None
            profile.save()

        else:
            logger.warning(f"No profile picture to delete for user {user_id}")

        return Response(
            {"message": "Profile picture removed"},
            status=status.HTTP_204_NO_CONTENT,
        )


# ---------------------------
# Upload Profile Picture (R2)
# ---------------------------

class ProfileImageUploadURLView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id
        content_type = request.data.get("contentType")

        logger.info(f"Avatar upload requested by user {user_id}")

        if not content_type:
            logger.error(f"Missing contentType from user {user_id}")

            return Response(
                {"error": "contentType is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_name = f"profiles/user_{user_id}/avatar.jpg"

        try:
            url = generate_presigned_url(file_name, content_type)

            public_url = (
                f"{settings.AWS_S3_ENDPOINT_URL}/"
                f"{settings.AWS_STORAGE_BUCKET_NAME}/"
                f"{file_name}"
            )

            logger.info(f"Generated upload URL for user {user_id}")

            return Response(
                {
                    "uploadUrl": url,
                    "publicUrl": public_url,
                }
            )

        except Exception as e:

            logger.exception(f"Failed to generate R2 upload URL: {e}")

            return Response(
                {"error": "Failed to generate upload URL"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
