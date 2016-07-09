from rest_framework.permissions import BasePermission

class OwnerorReadOnly(BasePermission):
    message="You cannot do this"
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user