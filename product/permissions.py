from rest_framework import permissions

class IsLaboratoryOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.laboratory.user == request.user
