from rest_framework import permissions
from .models import NoteSharedUsers


class IsNoteOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.created_by == request.user)


class HasNoteAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        mapping = NoteSharedUsers.objects.filter(note=obj)
        allow_user = mapping.exists() and request.user in mapping.first().shared_users.all()
        return (
            obj.created_by == request.user
            or allow_user
        )
