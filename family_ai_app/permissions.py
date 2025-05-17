from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows access to the owner of the object or an admin user.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_superuser or obj.user == request.user
    
    
class IsSenderOrAdmin(permissions.BasePermission):
    """
    Allows access only to the sender of the message or admin users.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_superuser or obj.sender == request.user


class IsOwnerOfNotification(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user