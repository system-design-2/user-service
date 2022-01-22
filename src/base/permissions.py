from django.conf import settings
from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Allows access only to Restaurant Manager users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name=settings.MANAGER).exists())


class IsEmployee(BasePermission):
    """
    Allows access only to Company Employee users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name=settings.EMPLOYEE).exists())
