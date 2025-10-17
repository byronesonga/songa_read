from rest_framework import permissions

class IsAdminOrLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_librarian() or user.is_admin()

class IsOwnerOrLibrarianOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if user.is_librarian() or user.is_admin():
            return True
        # assume object has user attribute
        return getattr(obj, "user", None) == user
