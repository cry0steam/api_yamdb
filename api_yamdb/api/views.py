from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions

from reviews.models import Review, Comments, Title
from api.serializers import ReviewSerializer, CommentsSerializer
from api.permissions import IsAuthorOrReadOnly


def get_needed_object(obj, model, id):
    return get_object_or_404(model, id=obj.kwargs.get(id))


class ReviewViewSet(viewsets.ModelViewSet):
    """Настройки вьюсета модели Review."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )
    ordering_fields = ('-pub_date',)

    def get_queryset(self):
        """Определяет необходимый набор queryset для сериализации."""
        return get_needed_object(self, Title, 'title_id').reviews.all()

    def perform_create(self, serializer):
        """Создание нового экземпляра модели после сериализации."""
        serializer.save(author=self.request.user,
                        title=get_needed_object(self, Title, 'title_id')
                        )


class CommentsViewSet(viewsets.ModelViewSet):
    """Настройки вьюсета модели Comments."""

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )
    ordering_fields = ('-pub_date',)

    def get_queryset(self):
        """Определяет необходимый набор queryset для сериализации."""
        return get_needed_object(self, Review, 'review_id').comments.all()

    def perform_create(self, serializer):
        """Создание нового экземпляра модели после сериализации."""
        serializer.save(author=self.request.user,
                        review=get_needed_object(self, Review, 'review_id')
                        )
