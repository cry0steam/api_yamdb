from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator  # type: ignore

from reviews.models import Category, Genre, Title, Review, Comments



class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор для категории.'''
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    '''Сериализатор для жанров.'''
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    '''Сериализатор для произведений.'''
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

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
