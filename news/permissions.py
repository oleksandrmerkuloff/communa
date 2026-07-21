from rest_framework import permissions

from membership.models import Membership
from membership.services import get_membership


# Later I'll change roles to fixed model bcs I don't like != Resident syntax
class CanViewNews(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return False
        
        return Membership.objects.filter(
            member=request.user,
            organization=obj.organization
        ).exists()


class CanCreateNews(permissions.BasePermission):
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


class CanEditNews(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "Patch" and request.method != "PUT":
            return False
        
        member = get_membership(
            user=request.user,
            organization_id=request.data.get("organization")
            )

        if not member:
            return False

        return member.role != Membership.MemberRole.RESIDENT


class CanDeleteNews(permissions.BasePermission):
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


class CanPublishNews():
    pass


class CanCreateTags(permissions.BasePermission):
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


class CanEditTags(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in ("PATCH", "PUT"):
            return False
        
        member = get_membership(
            user=request.user,
            organization_id=request.data.get("organization")
            )

        if not member:
            return False

        return member.role != Membership.MemberRole.RESIDENT


class CanDeleteTags(permissions.BasePermission):
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
