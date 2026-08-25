from django.apps import AppConfig


class PermissionsConfig(AppConfig):
    name = 'permissions'

    def ready(self):
        from . import signals
