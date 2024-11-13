from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    '''Проверка на администраторские доступы.'''
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    '''Проверка на администраторский доступ, иначе - только чтение.'''
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )
