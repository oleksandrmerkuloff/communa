from django.db import models


class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
