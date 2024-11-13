from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from reviews.models import Category, Genre, Title
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    '''Вспомогательный класс для категорий и жанров.'''
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category', 'genre', 'name', 'year')

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category,
            slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)
