from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions

from reviews.models import Review, Comments, Title
from api.serializers import ReviewSerializer, CommentsSerializer
from api.permissions import IsAuthorOrReadOnly


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
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создание нового экземпляра модели после сериализации."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


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
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """Создание нового экземпляра модели после сериализации."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
