from rest_framework import permissions

from membership.models import Membership
from membership.services import get_membership


class CanViewBudgets(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return False

        return Membership.objects.filter(
            member=request.user,
            organization=obj.organization
        ).exists()


class CanCreateBudgets(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return False

        if not request.user.is_authenticated:
            return False

        member = get_membership(
            user=request.user,
            organization_id=request.data.get("organization")
        )
        if not member:
            return False

        return member.role != Membership.MemberRole.RESIDENT


class CanEditdBudgets(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in ("PATCH", "PUT",):
            return False

        member = get_membership(
            user=request.user,
            organization_id=obj.organization.id
        )

        if not member:
            return False

        return member.role != Membership.MemberRole.RESIDENT
