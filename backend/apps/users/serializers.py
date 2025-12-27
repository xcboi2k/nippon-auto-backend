from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE_MB = 2

User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        credentials = {
            "email": attrs.get("email"),
            "password": attrs.get("password"),
        }
        return super().validate(attrs)
    
class SignupSerializer(serializers.Serializer):
    firstName = serializers.CharField(max_length=150)
    lastName = serializers.CharField(max_length=150)
    userName = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirmPassword"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirmPassword")

        user = User.objects.create_user(
            username=validated_data["userName"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["firstName"],
            last_name=validated_data["lastName"],
        )

        Profile.objects.create(
            user=user,
            firstName=validated_data["firstName"],
            lastName=validated_data["lastName"],
            username=validated_data["userName"],
            email=validated_data["email"],
        )

        return user
    
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "firstName",
            "lastName",
            "username",
            "email",
            "shopName",
            "location",
            "mobileNumber",
            "bio",
            "profilePicture",
        ]
        read_only_fields = ["username", "email"]
        
    def validate_profilePicture(self, image):
        if not image:
            return image

        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise serializers.ValidationError(
                "Only JPG and PNG images are allowed."
            )

        if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise serializers.ValidationError(
                f"Image size must be under {MAX_IMAGE_SIZE_MB}MB."
            )

        return image
    


class UploadURLSerializer(serializers.Serializer):
    fileName = serializers.CharField()
    contentType = serializers.CharField()

