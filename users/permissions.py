from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.request import Request


class UserPermission(permissions.BasePermission):
    """
        User is unable to create accounts. User is able to change/delete his own account.
        Superuser can do everything
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser

        return True

    def has_object_permission(self, request: HttpRequest | Request, view, obj):
        print(request.user)

        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True

        return request.user == obj
