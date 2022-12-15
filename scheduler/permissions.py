from rest_framework import permissions


class IsOwnerOrAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.profile.role == 'administrator' or request.user.profile.role == 'owner')
