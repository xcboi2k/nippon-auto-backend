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

# ---------------------------
# Health check
# ---------------------------
class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()

@extend_schema(responses=HealthCheckSerializer)
class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
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
        return self.request.user.profile


# ---------------------------
# JWT login using email
# ---------------------------
@extend_schema(
    request=EmailTokenObtainPairSerializer,
    examples=[
        OpenApiExample(
            'Sample Login',
            summary='Email/password input',
            value={'email': 'user@example.com', 'password': 'password123'},
            request_only=True,
        )
    ],
    responses={200: EmailTokenObtainPairSerializer},
)
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    
    
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
                "confirmPassword": "password123"
            },
            request_only=True,
        )
    ]
)
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )
        
        
# ---------------------------
# Delete Profile Picture
# ---------------------------
class DeleteProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        profile = request.user.profile

        if profile.profilePicture:
            profile.profilePicture.delete(save=False)
            profile.profilePicture = None
            profile.save()

        return Response(
            {"message": "Profile picture removed"},
            status=status.HTTP_204_NO_CONTENT
        )
        
        
# ---------------------------
# Upload Profile Picture
# ---------------------------
from .r2 import generate_presigned_url
class ProfileImageUploadURLView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_name = f"profiles/user_{request.user.id}/avatar.jpg"
        content_type = request.data["contentType"]

        url = generate_presigned_url(file_name, content_type)

        public_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_name}"

        return Response({
            "uploadUrl": url,
            "publicUrl": public_url,
        })