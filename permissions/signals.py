from django.db.models.signals import post_migrate
from django.dispatch import receiver

from core.permissions.codes import PermissionCode
from .models import Permission


@receiver(post_migrate)
def create_permissions(sender, **kwargs):
    if sender.name != "permissions":
        return

    codes = [
        value
        for name, value in vars(PermissionCode).items()
        if not name.startswith("_")
    ]

    for code in codes:
        Permission.objects.get_or_create(code=code)
