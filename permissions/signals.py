from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Permission
from core.permissions.codes import PermissionCode


@receiver(post_migrate, sender=Permission)
def sync_permissions_from_codes(sender, **kwargs):
    permission_codes = [
        val for key, val in PermissionCode.__dict__.items()
        if not key.startswith("__") and isinstance(val, str)
    ]

    for code in permission_codes:
        name = code.replace(".", " ").capitalize()
        Permission.objects.create(
            code=code,
            defaults={"name": name}
            )