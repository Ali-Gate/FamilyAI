from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows access to the owner of the object or an admin user.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_superuser or obj.user == request.user