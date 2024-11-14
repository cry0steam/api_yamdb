"""Модуль содержит URL настройки адрессов приложения API."""
from django.urls import include, path  # type: ignore
from rest_framework.routers import DefaultRouter  # type: ignore

from api.views import (
    ReviewViewSet, CategoryViewSet, CommentsViewSet, GenreViewSet, TitleViewSet
)


router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comment'
)
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
