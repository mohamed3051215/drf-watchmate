from rest_framework import permissions


class isAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        admin_permission = super().has_permission(request, view)
        return admin_permission or request.method == "GET"


class ReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user == obj.review_user
    