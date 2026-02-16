from rest_framework import serializers
from .models import Listing, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ["id", "image"]


class ListingSerializer(serializers.ModelSerializer):
    # Accept everything as string
    vehicle_type = serializers.CharField()
    engine_type = serializers.CharField()
    drivetrain = serializers.CharField()
    transmission = serializers.CharField()
    vehicle_model = serializers.CharField()
    price = serializers.CharField()
    year = serializers.CharField()
    kilometers = serializers.CharField()

    images = ListingImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Listing
        fields = [
            "id",
            "vehicle_type",
            "engine_type",
            "drivetrain",
            "transmission",
            "vehicle_model",
            "price",
            "year",
            "kilometers",
            "images",
            "uploaded_images",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate(self, attrs):
        try:
            attrs["price"] = float(attrs["price"])
            attrs["year"] = int(attrs["year"])
            attrs["kilometers"] = int(attrs["kilometers"])
        except ValueError:
            raise serializers.ValidationError(
                "Price must be decimal. Year and kilometers must be integers."
            )

        return attrs

    def validate_uploaded_images(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                "At least one image is required."
            )
        return value

    def create(self, validated_data):
        images_data = validated_data.pop("uploaded_images")

        listing = Listing.objects.create(
            user=self.context["request"].user,
            **validated_data
        )

        for image in images_data:
            ListingImage.objects.create(
                listing=listing,
                image=image
            )

        return listing

    def update(self, instance, validated_data):
        images_data = validated_data.pop("uploaded_images", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if images_data:
            instance.images.all().delete()
            for image in images_data:
                ListingImage.objects.create(
                    listing=instance,
                    image=image
                )

        return instance
