from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import serializers

from .serializers import EmailTokenObtainPairSerializer

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


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ProfileSerializer)
    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        })


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
