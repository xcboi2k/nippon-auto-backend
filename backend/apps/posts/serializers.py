from rest_framework import serializers
from .models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image"]


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        allow_empty=True,
        max_length=3,
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "images",
            "uploaded_images",
            "created_at",
            "updated_at",
        ]

    def validate_uploaded_images(self, images):
        if len(images) > 3:
            raise serializers.ValidationError("Maximum of 3 images allowed.")
        
        for img in images:
            if img.size > 3 * 1024 * 1024:
                raise serializers.ValidationError("Max 3MB per image.")

            if img.content_type not in ["image/jpeg", "image/png", "image/webp"]:
                raise serializers.ValidationError("Only JPG, PNG, WEBP allowed.")
        
        return images

    def create(self, validated_data):
        images = validated_data.pop("uploaded_images", [])

        if len(images) > 3:
            raise serializers.ValidationError("Max 3 images allowed.")

        post = Post.objects.create(**validated_data)

        for img in images:
            PostImage.objects.create(
                post=post,
                image=img
            )

        return post

    def update(self, instance, validated_data):
        images = validated_data.pop("uploaded_images", None)

        instance.content = validated_data.get("content", instance.content)
        instance.save()

        if images is not None:

            if len(images) > 3:
                raise serializers.ValidationError("Max 3 images allowed.")

            instance.images.all().delete()

            for image in images:
                PostImage.objects.create(
                    post=instance,
                    image=image
                )

        return instance

