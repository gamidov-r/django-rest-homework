from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """ Проверка пользователя на модератора """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()

class IsOwner(permissions.BasePermission):
    """ Проверка пользователя на владение объектом """
    def has_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False







