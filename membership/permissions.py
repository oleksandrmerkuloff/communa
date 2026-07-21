from rest_framework import permissions

from .models import Membership
from .services import get_membership


class CanViewMembership(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return False
        
        return Membership.objects.filter(
            member=request.user,
            organization=obj.organization
        ).exists()


class CanCreateMembership(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return False
        
        member = get_membership(
            user=request.user,
            organization_id=request.data.get("organization")
            )

        if not member:
            return False

        return member.role != Membership.MemberRole.RESIDENT


class CanEditMembership(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "PATCH" and request.method != "PUT":
            return False
        
        member = get_membership(
            user=request.user,
            organization_id=request.data.get("organization")
            )

        if not member:
            return False

        return member.role != Membership.MemberRole.RESIDENT


class CanDeleteMembership(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method != "DELETE":
            return False
        
        member = get_membership(
            user=request.user,
            organization_id=obj.organization.id
        )

        if not member:
            return False

        return member.role != Membership.MemberRole.RESIDENT


class CanChangeMemberRole(permissions.BasePermission):
    pass
