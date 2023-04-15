from rest_framework import permissions


class IsAdmin(permissions.BasePermissions):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return(
                request.user.role == 'admin' or request.user.is_superuser
            )
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return(
                request.user.role == 'admin' or request.user.is_superuser
            )
        return False


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    message = MSG_USR_NO_RIGHTS

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )
