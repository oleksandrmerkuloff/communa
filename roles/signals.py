from django.db.models.signals import post_save
from django.dispatch import receiver

from core.permissions.codes import PermissionCode
from organization.models import Organization
from permissions.models import Permission
from .models import Role


@receiver(post_save, sender=Organization)
def create_system_roles_for_organization(sender, instance, created, **kwargs):
    if not created:
        return

    head_role, _ = Role.objects.get_or_create(
        name="Голова ОСББ",
        organization=instance,
        defaults={"is_system": True}
    )
    all_permissions = Permission.objects.all()
    head_role.permissions.set(all_permissions)

    resident_role, _ = Role.objects.get_or_create(
        name="Голова ОСББ",
        organization=instance,
        defaults={"is_system": True}
    )
    # Change later permissions for resident
    resident_permissions = Permission.objects.filter(
        code__in=[
            PermissionCode.NEWS_READ,
            PermissionCode.ORGANIZATIONS_READ,
            PermissionCode.MEMBERSHIPS_READ,
            PermissionCode.ACCOUNTING_READ,
        ]
    )
    resident_role.permissions.set(resident_permissions)
