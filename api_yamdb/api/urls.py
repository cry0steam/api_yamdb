"""Модуль содержит URL настройки адрессов приложения API."""
from django.urls import include, path  # type: ignore
from rest_framework.routers import DefaultRouter  # type: ignore

from api.views import (
    ReviewViewSet, CommentsViewSet
)


router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comment'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]