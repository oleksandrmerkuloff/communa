from rest_framework import permissions
from permissions.models import Permission
from membership.services import get_membership


class HasPermission(permissions.BasePermission):
    """
    Кастомний дозволяючий клас для перевірки наявності прав (RBAC) у користувача 
    в межах конкретної організації.
    
    Для використання у ViewSet задайте атрибут `required_permission`:
    
    class NewsViewSet(viewsets.ModelViewSet):
        permission_classes = [HasPermission]
        required_permission = PermissionCode.NEWS_CREATE
    """
    
    required_permission = None

    def _get_organization_id(self, request, view, obj=None):
        """
        Отримує ID організації з kwargs URL, об'єкта або параметрів запиту.
        """
        org_id = view.kwargs.get('organization_pk') or view.kwargs.get('organization_id')
        if org_id:
            return org_id

        if obj is not None:
            if hasattr(obj, 'organization_id'):
                return obj.organization_id
            elif hasattr(obj, 'organization'):
                return obj.organization.id

        org_id = request.query_params.get('organization_id') or request.data.get('organization_id')
        if org_id:
            return org_id

        return None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        required_perm = getattr(view, 'required_permission', self.required_permission)
        if not required_perm:
            return True

        org_id = self._get_organization_id(request, view)
        if not org_id:
            return False

        membership = get_membership(request.user, org_id)
        if not membership or not membership.role:
            return False

        return membership.role.permissions.filter(code=required_perm).exists()

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        required_perm = getattr(view, 'required_permission', self.required_permission)
        if not required_perm:
            return True

        org_id = self._get_organization_id(request, view, obj=obj)
        if not org_id:
            return False

        membership = get_membership(request.user, org_id)
        if not membership or not membership.role:
            return False

        return membership.role.permissions.filter(code=required_perm).exists()
