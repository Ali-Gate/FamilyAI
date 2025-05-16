from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow object access to the owner or an admin.
    """

    def has_object_permission(self, request, view, obj):
        # Allow access if the user is admin
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Otherwise, allow access only if the user owns the object
        return obj.user == request.user