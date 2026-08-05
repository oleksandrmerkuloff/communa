from rest_framework import permissions

from membership.models import Membership
from membership.services import get_membership


class CanViewBudget(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return False

        return Membership.objects.filter(
            member=request.user,
            organization=obj.organization
        ).exists()


class CanCreateBudget(permissions.BasePermission):
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


class CanEditBudget(permissions.BasePermission):
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


class CanDeleteBudget(permissions.BasePermission):
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


class CanViewIncome(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return False

        return Membership.objects.filter(
            member=request.user,
            organization=obj.organization
        ).exists()


class CanCreateIncome(permissions.BasePermission):
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


class CanEditIncome(permissions.BasePermission):
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


class CanDeleteIncome(permissions.BasePermission):
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


class CanViewExpense(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return False

        return Membership.objects.filter(
            member=request.user,
            organization=obj.organization
        ).exists()


class CanCreateExpense(permissions.BasePermission):
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


class CanEditExpense(permissions.BasePermission):
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


class CanDeleteExpense(permissions.BasePermission):
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


class CanViewCategory(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return False

        return Membership.objects.filter(
            member=request.user,
            organization=obj.organization
        ).exists()


class CanCreateCategory(permissions.BasePermission):
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


class CanEditCategory(permissions.BasePermission):
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


class CanDeleteCategory(permissions.BasePermission):
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
