from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    required_permission = None

    def has_permission(self, request, view):
        membership = get_membership(
            request.user,
            request.organization,
        )

        return membership.role.permissions.filter(
            code=self.required_permission
        ).exists()
