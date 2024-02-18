from rest_framework import permissions


class IsNoteOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.created_by == request.user)


class HasNoteAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.created_by == request.user
            # or request.user in obj.shared_users.all()
        )
