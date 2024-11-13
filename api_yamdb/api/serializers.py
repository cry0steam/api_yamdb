"""Модуль содержит настройки сериализаторов приложения API."""
from rest_framework import serializers   # type: ignore
from rest_framework.validators import UniqueTogetherValidator  # type: ignore

from reviews.models import Review, Comments


class ReviewSerializer(serializers.ModelSerializer):   
    """Настройки сериализатора модели Review."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        """Метаданные сериализатора отзывов."""

        fields = '__all__'
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    """Настройки сериализатора модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Метаданные сериализатора комментариев."""

        fields = '__all__'
        model = Comments
