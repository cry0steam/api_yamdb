from rest_framework import serializers
from reviews.models import Category, Comments, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Класс сериализатора для произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
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


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserAdminSerializer(BaseUserSerializer):
    pass


class UserNotAdminSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        read_only_fields = ('role',)
