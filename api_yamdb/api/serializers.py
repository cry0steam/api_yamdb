from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
