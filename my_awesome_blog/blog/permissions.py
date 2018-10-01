from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    message = 'Not an author.'

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or \
               request.user == obj.author
