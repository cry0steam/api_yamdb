"""Модуль содержит настройки правил запретов API."""
from rest_framework import permissions  # type: ignore


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Класс в котором проверяется пользователь.

    Проверяется является ли пользователь владельцем объекта,
    разрещая ему редактировать его.
    """

    def has_object_permission(self, request, view, obj):
        """Метод проверяет является ли user автором, модератором или админом.

        Безопасный ли метод запроса
        """
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                )
