from rest_framework import permissions

from membership.models import Membership
from membership.services import get_membership


# Actually I don't know if I need to make this perm right now bcs user need to be only auth
class CanCreateOrganization(permissions.BasePermission):
    pass


class CanEditOrganization(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in ("PATCH", "PUT"):
            return False
        
        member = get_membership(
            user=request.user,
            organization_id=obj.id
        )

        if not member:
            return False
        
        return member.role != Membership.MemberRole.RESIDENT


class CanDeleteOrganization(permissions.BasePermission):
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
