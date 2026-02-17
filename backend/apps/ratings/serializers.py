from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    reviewer = serializers.SerializerMethodField()
    rating = serializers.CharField()

    class Meta:
        model = Rating
        fields = [
            "id",
            "reviewer",
            "rated_user",
            "rating",
            "review",
            "created_at",
        ]
        read_only_fields = ["reviewer", "created_at"]

    def get_reviewer(self, obj):
        return obj.reviewer.username

    def validate_rating(self, value):
        rating_value = int(value)

        if rating_value < 1 or rating_value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating_value

    def validate(self, attrs):
        request_user = self.context["request"].user
        if attrs["rated_user"] == request_user:
            raise serializers.ValidationError(
                "You cannot rate yourself."
            )
        return attrs
